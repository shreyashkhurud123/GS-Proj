from copy import deepcopy
from datetime import timedelta, datetime, timezone

import jwt

from app.config import settings


class VxJWTUtils:

    @staticmethod
    def create_access_token(data: dict, expiry_delta: int = None) -> str:
        """
            Function to create a JWT token
        """

        to_encode = deepcopy(data)

        if expiry_delta:
            expiry_in = datetime.now(timezone.utc) + timedelta(expiry_delta)
        else:
            expiry_in = datetime.now(timezone.utc) + timedelta(minutes=settings)

        print("Creating access token", expiry_in)
        print("Creating access token", expiry_in.isoformat())

        to_encode.update({"exipry": expiry_in.isoformat()})

        encoded_jwt = jwt.encode(payload=to_encode, key=settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

        return encoded_jwt

