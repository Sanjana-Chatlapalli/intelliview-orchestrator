"""Shared API-token, password, and JWT auth dependencies."""

import logging
from datetime import datetime, timedelta, timezone

from fastapi import Header, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext

from config import (
    API_TOKEN,
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_ALGORITHM,
    JWT_SECRET_KEY,
)

logger = logging.getLogger(__name__)

# Password hashing configuration
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """Hash a plain-text password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plain-text password against a bcrypt hash."""
    return pwd_context.verify(password, password_hash)


def require_token(x_api_token: str | None = Header(default=None)) -> None:
    """Dependency that requires a valid API token."""
    if not API_TOKEN or API_TOKEN == "dev-token-change-me":
        logger.debug("Using default API token — set API_TOKEN in production")

    if x_api_token != API_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="invalid or missing API token",
        )


def create_access_token(data: dict) -> str:
    """Generate a signed JWT access token."""

    to_encode = data.copy()

    now = datetime.now(timezone.utc)
    expire = now + timedelta(
        minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {
            "exp": expire,
            "iat": now,
        }
    )

    return jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


def verify_access_token(token: str):
    """Verify and decode a JWT."""

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )

        return payload

    except JWTError:
        return None