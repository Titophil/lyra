from . import models
from .db import database
from . import SessionLocal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite:///./lib/db/schema.db"

engine = create_engine(
    DATABASE_URL, connect_args = {"check_same_thread": False}

)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)