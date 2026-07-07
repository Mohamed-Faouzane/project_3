import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)    #  creates the connection to PostgreSQL using your .env URL. Think of it as opening the door to the database.

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)   # a factory that creates database sessions. Each request to your API gets its own session (its own "conversation" with the database).

Base = declarative_base()   # the base class all your database models will inherit from. SQLAlchemy uses it to track what tables exist.

def get_db():               # get_db() — a dependency FastAPI will inject into your endpoints.
    db = SessionLocal()
    try:
        yield db            # The yield makes it a generator — it opens a session, gives it to the endpoint, then closes it when done.
    finally:
        db.close()          # always close it after, even if an error occurred