from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from flask import current_app


def get_engine():
    engine = create_engine(
        current_app.config["DATABASE_URI"],
        pool_size=20,
        max_overflow=0,
    )
    return engine


def get_session_local():
    engine = get_engine()
    return sessionmaker(bind=engine)


Base = declarative_base()


@contextmanager
def get_db_session():
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
