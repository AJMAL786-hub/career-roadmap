from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "CareerPath AI"
    DATABASE_URL: str = "sqlite:///./careerpath.db"
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    # Short-lived access token (defense-in-depth: limits damage if leaked)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # Long-lived refresh token used only to mint new access tokens
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    # Session cookie names
    ACCESS_COOKIE: str = "careerpath_access"
    REFRESH_COOKIE: str = "careerpath_refresh"
    CSRF_COOKIE: str = "careerpath_csrf"
    # Cookies dropped over HTTPS only; set False for plain-HTTP local dev
    COOKIE_SECURE: bool = False
    # Error paths mitigate CSRF via SameSite + a double-submit CSRF token header.
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:8000,http://127.0.0.1:8000,http://localhost:3000,http://127.0.0.1:3000,*"

    @property
    def CORS_ORIGINS_LIST(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    class Config:
        env_file = ".env"


settings = Settings()
