from __future__ import annotations

import logging
import platform
import sys
from typing import Callable
from typing import Optional

import structlog
from ddtrace import tracer
from ddtrace.runtime import RuntimeMetrics
from structlog.processors import CallsiteParameter
from structlog.types import EventDict
from structlog.types import Processor

from artemis_common.consts import artemis_env
from artemis_common.consts import is_artemis_debug
from artemis_common.consts import is_prod_env
from artemis_common.logging import DatadogLoggingHandler
from artemis_common.models import LoggingCenterModel


def get_log_level(
    is_debug: bool = False,
) -> int:
    """
    is_debug: set log level to DEBUG
        this argument has the highest priority

    if `ARTEMIS_DEBUG` environment variable is true
        it will set log level to DEBUG

    Default log level: INFO
    """
    if is_debug:
        return logging.DEBUG
    if is_artemis_debug:
        return logging.DEBUG

    return logging.INFO


def is_use_console(
    is_prod: bool = False,
    is_console: bool = False,
) -> bool:
    """
    is_prod: set console logging to False
    is_console: set if use json logging or console logging

    Default is to use json logging
    """
    if is_prod:
        return False
    return is_console


def drop_color_message_key(_, __, event_dict: EventDict) -> EventDict:
    event_dict.pop('color_message', None)
    return event_dict


def tracer_injection(_, __, event_dict: EventDict) -> EventDict:
    # get correlation ids from current tracer context
    span = tracer.current_span()
    trace_id, span_id = (span.trace_id, span.span_id) if span else (None, None)

    dd = event_dict.get('dd', {})
    dd['trace_id'] = str(trace_id or 0)
    dd['span_id'] = str(span_id or 0)

    event_dict['dd'] = dd
    return event_dict


def datadog_injection(
    env: str,
    service: str,
    version: str,
) -> Callable:
    def service_injection_wrapper(_, __, event_dict: EventDict) -> EventDict:
        dd = event_dict.get('dd', {})
        dd['service'] = dd.get('service', service)
        dd['env'] = dd.get('env', env)
        dd['version'] = dd.get('version', version)

        event_dict['dd'] = dd
        return event_dict
    return service_injection_wrapper


def system_metadata_injection(_, __, event_dict: EventDict) -> EventDict:
    event_dict['host_name'] = event_dict.get('host_name', platform.node())
    event_dict['system'] = event_dict.get('system', platform.system())
    event_dict['platform'] = event_dict.get('platform', platform.platform())
    event_dict['python_version'] = event_dict.get('python_version', platform.python_version())
    return event_dict


def _reconfigure_uvicorn_logger():
    for _log in ['uvicorn', 'uvicorn.error']:
        # Clear the log handlers for uvicorn loggers, and enable propagation
        # so the messages are caught by our root logger and formatted correctly
        # by structlog
        logging.getLogger(_log).handlers.clear()
        logging.getLogger(_log).propagate = True

    # Since we re-create the access logs ourselves, to add all information
    # in the structured log (see the `logging_middleware` in main.py), we clear
    # the handlers and prevent the logs to propagate to a logger higher up in the
    # hierarchy (effectively rendering them silent).
    logging.getLogger('uvicorn.access').handlers.clear()
    logging.getLogger('uvicorn.access').propagate = False


def _handle_exception_hook(exc_type, exc_value, exc_traceback):
    """
    Log any uncaught exception instead of letting it be printed by Python
    (but leave KeyboardInterrupt untouched to allow users to Ctrl+C to stop)
    See https://stackoverflow.com/a/16993115/3641865
    """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    root_logger = logging.getLogger()
    root_logger.error(
        'Uncaught exception', exc_info=(exc_type, exc_value, exc_traceback),
    )


def setup_logging(
    version: str,
    is_debug: bool = False,
    is_console: bool = False,
    logging_center: Optional[LoggingCenterModel] = None,
):
    log_level = get_log_level(is_debug=is_debug)
    use_console = is_use_console(is_prod=is_prod_env, is_console=is_console)
    service_name = None if not logging_center else logging_center.name

    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_log_level_number,
        structlog.processors.CallsiteParameterAdder([
            CallsiteParameter.PATHNAME,
            CallsiteParameter.FILENAME,
            CallsiteParameter.MODULE,
            CallsiteParameter.FUNC_NAME,
            CallsiteParameter.LINENO,
            CallsiteParameter.THREAD,
            CallsiteParameter.THREAD_NAME,
            CallsiteParameter.PROCESS,
            CallsiteParameter.PROCESS_NAME,
        ]),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.stdlib.ExtraAdder(),
        drop_color_message_key,
        tracer_injection,
        datadog_injection(
            env=artemis_env,
            service=service_name,
            version=version,
        ),
        system_metadata_injection,
        structlog.processors.TimeStamper(fmt='iso', utc=True),
        structlog.processors.StackInfoRenderer(),
    ]

    if not use_console:
        shared_processors.append(structlog.processors.EventRenamer(to='message'))
        # Format the exception only for JSON logs, as we want to pretty-print them when
        # using the ConsoleRenderer instead of JSONRenderer
        shared_processors.append(structlog.processors.format_exc_info)

    structlog.configure(
        processors=shared_processors + \
        # Must be the last processor before calling `ProcessorFormatter`.
        [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    if use_console:
        log_renderer = structlog.dev.ConsoleRenderer()
    else:
        log_renderer = structlog.processors.JSONRenderer()

    formatter = structlog.stdlib.ProcessorFormatter(
        # These run ONLY on `logging` entries that do NOT originate within structlog.
        foreign_pre_chain=shared_processors,
        # These run on ALL entries after the pre_chain is done.
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            log_renderer,
        ],
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(stream_handler)

    if logging_center:
        tcp_handler = DatadogLoggingHandler()
        tcp_handler.setFormatter(formatter)
        root_logger.addHandler(tcp_handler)

    _reconfigure_uvicorn_logger()

    sys.excepthook = _handle_exception_hook


def enable_runtime_metrics(logging_center: LoggingCenterModel):
    stats_url = f'{logging_center.host}:{logging_center.stats_port}'
    RuntimeMetrics.enable(tracer=tracer, dogstatsd_url=stats_url)
