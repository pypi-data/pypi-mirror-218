from __future__ import annotations

import logging

from datadog_api_client import ApiClient
from datadog_api_client import Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.content_encoding import ContentEncoding
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem

from artemis_common.consts import ArtemisEnvironment


class DatadogLoggingHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        env_vars = ArtemisEnvironment()
        self.configuration = Configuration()
        self.version = env_vars.version
        self.service = env_vars.service
        self.env = env_vars.artemis_env

    def emit(self, record):
        try:
            raw_log = self.format(record)
            log_item = HTTPLogItem(
                ddsource='python',
                ddtags=f'env:{self.env},version:{self.version}',
                message=raw_log,
                service=self.service,
            )
            body = HTTPLog([log_item])

            with ApiClient(self.configuration) as api_client:
                api_instance = LogsApi(api_client)
                api_instance.submit_log(content_encoding=ContentEncoding.GZIP, body=body)

        except Exception:
            self.handleError(record)
