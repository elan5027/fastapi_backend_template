import logging
import os

from typing import Any, Dict
from app.core.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    title: str = "FastAPI"
    version: str = "1.0.0"
    base_url: str = "https://api.dev.dns.run/"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"

    database_url: str
    max_connection_count: int = 10
    db_schema: str = "public"

    logging_level: int = logging.INFO

    seed_key: str
    user_key: str

    class Config:
        validate_assignment = True

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "version": self.version,
            "servers": [{"url": self.base_url, "description": os.getenv("ENV", "local")}],
            "docs_url": self.docs_url,
            "redoc_url": self.redoc_url,
        }

    def configure_logging(self) -> None:
        logging.basicConfig()
        logger = logging.getLogger("app")
        logger.setLevel(self.logging_level)
