from contextvars import ContextVar, Token
from enum import Enum

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from sqlalchemy.sql.expression import Delete, Insert, Update
from app.models.db.base import Base
from app.core.config import get_app_settings

session_context: ContextVar[str] = ContextVar("session_context")

class EngineType(Enum):
    WRITER = "writer"
    READER = "reader"

def get_session_context() -> str:
    try:
        return session_context.get()
    except LookupError:
        token = set_session_context("request")
        return token

def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)

def set_engines() -> dict:
    engine = create_engine(
        get_app_settings().database_url,
        pool_size=20,
        echo=True,
        pool_pre_ping=True,
        max_overflow=10,
    )
    Base.metadata.create_all(bind=engine)
    return {
        EngineType.WRITER: engine.execution_options(isolation_level="SERIALIZABLE"),
        EngineType.READER: engine,
    }

engines = set_engines()

class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kw):
        if self._flushing or isinstance(clause, (Update, Delete, Insert)):
            return engines[EngineType.WRITER]
        else:
            return engines[EngineType.READER]


session_factory = sessionmaker(
    class_=RoutingSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

session = scoped_session(
    session_factory=session_factory,
    scopefunc=get_session_context,
)
