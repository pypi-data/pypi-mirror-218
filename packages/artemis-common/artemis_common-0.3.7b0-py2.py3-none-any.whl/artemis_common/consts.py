from __future__ import annotations

from enum import Enum

from distutils.util import strtobool as str_to_bool
from pydantic import BaseSettings
from pydantic import Field
from pydantic import SecretStr


ARTEMIS_DAL_API_KEY_NAME = 'x-artemis-dal-api-key'


class ArtemisEnvironment(BaseSettings):
    artemis_env: str = 'dev'
    artemis_debug: str = 'False'
    version: str
    service: str = Field(..., env='dd_service')


artemis_env = ArtemisEnvironment().artemis_env
is_prod_env = artemis_env == 'prod'
is_artemis_debug = str_to_bool(ArtemisEnvironment().artemis_debug)


class _EnvironmentVariables(BaseSettings):
    artemis_dal_api_key: SecretStr = Field(
        ...,
        env=f'{artemis_env}_ARTEMIS_DAL_API_KEY',
    )
