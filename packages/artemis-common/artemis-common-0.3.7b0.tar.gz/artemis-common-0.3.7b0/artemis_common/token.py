from __future__ import annotations

from datetime import datetime

import jwt

from .config import read_pem
from .models import JWTDecodedPayloadModel


ALGORITHMS = ['RS256']
PEM = read_pem()


def decode_token(token: str) -> JWTDecodedPayloadModel:
    if not token:
        raise jwt.exceptions.InvalidTokenError('Missing token!')
    raw_payload = jwt.decode(
        jwt=token,
        key=PEM,
        algorithms=ALGORITHMS,
    )
    payload = JWTDecodedPayloadModel(**raw_payload)
    utc_now = datetime.utcnow()

    if utc_now >= payload.exp:
        raise jwt.exceptions.ExpiredSignatureError()

    return payload
