from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Settings, get_settings
from db.models import Base


def get_db(settings: Settings = Depends(get_settings)):
    if settings.TESTING:
        engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True, connect_args={
                               "check_same_thread": False})
    else:
        engine = create_engine(settings.SQLALCHEMY_DATABASE_URI,
                               echo=False, pool_recycle=settings.POOL_RECYCLE)
    session = sessionmaker(bind=engine)
    session = session()
    if settings.TESTING:
        Base.metadata.create_all(bind=engine)
    try:
        yield session
    finally:
        session.close()
