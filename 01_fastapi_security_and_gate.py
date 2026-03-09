"""Portfolio sample: JWT auth + global access gate middleware."""

from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.access_gate import verify_access_gate_token
from app.core.config import get_settings
from app.services.user_service import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    settings = get_settings()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    user = get_user_by_id(str(user_id))
    if not user or not user.is_active:
        raise credentials_exception
    return user


class AccessGateMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        settings = get_settings()
        if not settings.server_access_password:
            return await call_next(request)

        path = request.url.path
        public_paths = {"/login", "/login/config", "/logout", "/api/v1/health", "/api/v1/health/"}
        public_prefixes = ("/static/", "/api/v1/auth/")

        if request.method == "OPTIONS" or path in public_paths or path.startswith(public_prefixes):
            return await call_next(request)

        token = request.cookies.get(settings.server_access_cookie_name)
        if token and verify_access_gate_token(token, settings.secret_key, settings.algorithm):
            return await call_next(request)

        if path.startswith("/api/"):
            return JSONResponse(status_code=401, content={"detail": "Access login required at /login"})

        return RedirectResponse(url="/login", status_code=307)
