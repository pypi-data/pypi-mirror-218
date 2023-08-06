from __future__ import annotations

from fastapi import Request
from fastapi import Response
from pydantic import BaseModel


class LoggingCenterModel(BaseModel):
    name: str
    host: str
    stats_port: int


__all__ = [
    LoggingCenterModel.__name__,
]
