    # from datetime import datetime, UTC, timedelta
    #
    # from jwt import jwt
    #
    # from core.config import settings
    #
    #
    # def create_access_token(data: dict, expires_delta: timedelta | None = None):
    #     to_encode = data.copy()
    #     if expires_delta:
    #         expire = datetime.now(UTC) + expires_delta
    #     else:
    #         expire = datetime.now(UTC) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_TIME)
    #     to_encode.update({"exp": expire})
    #     encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    #     return encoded_jwt