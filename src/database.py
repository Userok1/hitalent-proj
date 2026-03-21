from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv(".env")

# from setup import setup

engine = create_engine(
    # url=setup.database_url,
    url = os.getenv("DATABASE_URL")
)

Session_local = sessionmaker(autoflush=False, expire_on_commit=False, bind=engine)


def get_session():
    try:
        session = Session_local()
        yield session
    finally:
        session.close()
    

class Base(DeclarativeBase):
    pass