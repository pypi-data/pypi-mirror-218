from __future__ import annotations

from time import perf_counter
from typing import Callable
from uuid import uuid4

import structlog
from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from starlette.middleware.base import BaseHTTPMiddleware
from structlog.contextvars import bind_contextvars
from structlog.contextvars import clear_contextvars

from artemis_common.server import get_client_address


REQUEST_KEY = 'REQUEST'
RESPONSE_KEY = 'RESPONSE'


class AsyncIteratorWrapper:
    def __init__(self, obj):
        self._it = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        *,
        logger: structlog.BoundLogger,
    ) -> None:
        self._logger = logger
        super().__init__(app)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        request_id = str(uuid4()).replace('-', '')
        client_address = get_client_address(request)

        clear_contextvars()
        bind_contextvars(
            request_id=request_id,
            client_address=client_address,
        )

        await self._log_request(request, request_id)

        start_time = perf_counter()
        response = await self._execute_request(request, call_next, request_id)
        end_time = perf_counter()

        process_time = round(end_time - start_time, 4)
        await self._log_response(response, request, request_id, process_time)

        return response

    async def _execute_request(
        self,
        request: Request,
        call_next: Callable,
        request_id: str,
    ) -> Response:
        try:
            response = await call_next(request)
            return response

        except Exception as ex:
            message = 'Failed to process response'
            self._logger.exception(
                message,
                http_transaction_type=RESPONSE_KEY,
                request_method=request.method,
                exc_message=str(ex),
            )
            raise

    async def _log_request(
        self,
        request: Request,
        request_id: str,
    ):
        message = f'Request {request.method} {request.url}'
        self._logger.info(
            message,
            http_transaction_type=REQUEST_KEY,
            request_method=request.method,
            request_headers=dict(request.headers),
            request_path=request.url.path,
            request_query=request.url.query,
        )

    async def _log_response(
        self,
        response: Response,
        request: Request,
        request_id: str,
        process_time: float,
    ):
        response_body = [section async for section in response.__dict__['body_iterator']]
        response.__setattr__(
            'body_iterator', AsyncIteratorWrapper(response_body),
        )

        response_length = 0
        for response_item in response_body:
            response_length += len(response_item)

        message = f'Response {request.method} {request.url}'
        self._logger.info(
            message,
            http_transaction_type=RESPONSE_KEY,
            request_method=request.method,
            response_time=process_time,
            response_length=response_length,
            status_code=response.status_code,
        )
