
from typing import Callable
from fastapi import FastAPI
from dependency_injector.wiring import inject
from sqlalchemy import text

from app.db.session import session
from app.core.settings.app import AppSettings


def create_start_app_handler(
    app: FastAPI,
    settings: AppSettings,
) -> Callable:
    @inject
    def start_app() -> None:
        # Use a session to verify database connectivity
        db_session = session()
        try:
            db_session.execute(text("SELECT 1"))
            print("Database connection established successfully.")
        except Exception as e:
            print(f"Failed to establish database connection: {e}")
        finally:
            db_session.close()

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    def stop_app() -> None:
        session.close_all()

    return stop_app
