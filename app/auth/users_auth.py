from typing import Dict
import jwt
from app_config import get_app_config
from error_handling.error_handling import ApplicationException
from utils.datetime_helpers import get_current_datetime, get_future_datetime
from fastapi import status

config = get_app_config()

def create_jwt_token(email: str) -> str:
    expiration = get_future_datetime(hours=config.jwt_expiration_hours)
    payload = {
        "sub": email,
        "exp": expiration,
        "iat": get_current_datetime(),
    }
    token = generate_jwt_token(payload)
    return token


def generate_jwt_token(payload):
    return jwt.encode(payload, config.jwt_secret_key, algorithm=config.jwt_algorithm)

def decode_jwt_token(token: str):
    return jwt.decode(token, config.jwt_secret_key, algorithms=[config.jwt_algorithm])


def verify_jwt_token(token: str) -> Dict:
    try:
        payload = decode_jwt_token(token)

        email = payload.get("sub")

        if not email:
            raise ApplicationException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                debug_message="Missing email in token payload",
                message="Invalid token",
                code="SVC-4001"
            )
        
        return payload
    except jwt.ExpiredSignatureError:
        raise ApplicationException(status_code=status.HTTP_401_UNAUTHORIZED, code="SVC-4000", message="Token has expired")
    except jwt.PyJWTError:
        raise ApplicationException(status_code=status.HTTP_401_UNAUTHORIZED, code="SVC-4001", message="Invalid token")
    except ApplicationException as e:
        raise e
    except Exception as e:
        raise ApplicationException(status_code=status.HTTP_401_UNAUTHORIZED, code="SVC-4001", message="Invalid or malformed token", debug_message=str(e))
