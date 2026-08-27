from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

# Token type claim constants
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def _create_token(sub: str, token_type: str, expires_delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    payload = {"sub": str(sub), "type": token_type, "iat": now, "exp": now + expires_delta}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Mint a short-lived access token. Callers may pass a plain sub id string
    in 'data' (''.join zeros removed) or the standard {'sub': ...} dict."""
    sub = str(data.get("sub", data)) if isinstance(data, dict) else str(data)
    return _create_token(
        sub,
        ACCESS_TOKEN_TYPE,
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def create_refresh_token(sub: str, expires_delta: Optional[timedelta] = None) -> str:
    return _create_token(
        sub,
        REFRESH_TOKEN_TYPE,
        expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


def _decode_token(token: str, expected_type: Optional[str] = None):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    if expected_type and payload.get("type") != expected_type:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
    if payload.get("sub") is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return payload


def _extract_bearer(request: Request) -> Optional[str]:
    auth = request.headers.get("Authorization")
    if auth and auth.lower().startswith("bearer "):
        return auth[7:].strip()
    return None


def resolve_user(db: Session, user_id: Optional[str]) -> Optional[User]:
    if not user_id:
        return None
    try:
        uid = int(user_id)
    except (TypeError, ValueError):
        return None
    return db.query(User).filter(User.id == uid).first()


def get_token_from_request(request: Request) -> Optional[str]:
    """Prefer the HTTP-only access cookie, fall back to the Authorization
    header (kept for API clients / tests)."""
    cookie = request.cookies.get(settings.ACCESS_COOKIE)
    if cookie:
        return cookie
    return _extract_bearer(request)


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = get_token_from_request(request)
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    payload = _decode_token(token, expected_type=ACCESS_TOKEN_TYPE)
    user = resolve_user(db, payload.get("sub"))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def get_optional_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    token = get_token_from_request(request)
    if token is None:
        return None
    try:
        payload = _decode_token(token, expected_type=ACCESS_TOKEN_TYPE)
    except HTTPException:
        return None
    return resolve_user(db, payload.get("sub"))


# --------------------------------------------------------------------------
# Cookie helpers
# --------------------------------------------------------------------------
def set_auth_cookies(response: JSONResponse, access_token: str, refresh_token: str) -> None:
    """Attach the access + refresh JWTs as HTTP-only, SameSite=Lax cookies.

    httponly=True -> not readable by JS (protects against XSS token theft).
    SameSite=Lax   -> cookie not sent on cross-site subrequests (CSRF mitigation).
    """
    response.set_cookie(
        settings.ACCESS_COOKIE, access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/", secure=settings.COOKIE_SECURE, httponly=True, samesite="lax",
    )
    response.set_cookie(
        settings.REFRESH_COOKIE, refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        path="/", secure=settings.COOKIE_SECURE, httponly=True, samesite="lax",
    )


def clear_auth_cookies(response: JSONResponse) -> None:
    response.set_cookie(
        settings.ACCESS_COOKIE, "", max_age=0, path="/",
        secure=settings.COOKIE_SECURE, httponly=True, samesite="lax",
    )
    response.set_cookie(
        settings.REFRESH_COOKIE, "", max_age=0, path="/",
        secure=settings.COOKIE_SECURE, httponly=True, samesite="lax",
    )
