from __future__ import annotations

import json
import logging

from ddtrace import patch_all

from .config import CONFIG_DIR
from .config import get_config
from .config import read_pem

patch_all()

uvicorn_disable_logging_file = CONFIG_DIR.joinpath('uvicorn_disable_logging.json')
uvicorn_disable_logging_config = json.loads(uvicorn_disable_logging_file.read_text())
logging.config.dictConfig(uvicorn_disable_logging_config)
