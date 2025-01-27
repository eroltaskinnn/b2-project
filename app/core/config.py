import os
from pathlib import Path
from sys import modules

from pydantic import BaseSettings


BASE_DIR = Path(__file__).parent.resolve()


class Settings(BaseSettings):
    """Application settings."""
    class Config:
        env_file = f"{BASE_DIR}/.env"
        env_file_encoding = "utf-8"

    ENV: str = "dev"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    _BASE_URL: str = f"https://{HOST}:{PORT}"
    # quantity of workers for uvicorn
    WORKERS_COUNT: int = 1

    # Enable uvicorn reloading
    RELOAD: bool = False

    # Database settings
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))
    DB_USER: str = os.getenv("DB_USER", "admin")
    DB_PASS: str = os.getenv("DB_PASS", "admin")
    _DB_BASE: str = os.getenv("DB_BASE", "test3")
    DB_ECHO: bool = False

    MAILHOG_HOST: str = os.getenv("MAIL_SERVER", "localhost")
    MAILHOG_PORT: str = os.getenv("MAIL_SERVER_PORT", "1025")

    CELERY_BROKER_URL: str = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_BACKEND_URL: str = os.getenv('CELERY_BACKEND_URL', 'redis://localhost:6379/0')

    MAIL_SENDER="your_sender_email@domain.com"
    SYSTEM_ADMIN="your_admin_email@domain.com"
    @property
    def DB_BASE(self):
        return self._DB_BASE

    @property
    def BASE_URL(self) -> str:
        return self._BASE_URL if self._BASE_URL.endswith("/") else f"{self._BASE_URL}/"

    @property
    def DB_URL(self) -> str:
        """
        Assemble Database URL from settings.

        :return: Database URL.
        """

        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_BASE}"



class TestSettings(Settings):
    @property
    def DB_BASE(self):
        return f"{super().DB_BASE}_test"



settings = TestSettings() if "pytest" in modules else Settings()
