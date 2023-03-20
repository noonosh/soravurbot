from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

load_dotenv()



url_object = URL.create(
    "postgresql+psycopg2",
    username=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME")
)

engine = create_engine(url_object, echo=True)

session = Session(engine)

class Base(DeclarativeBase):
    def __tablename__(cls):
        return cls.__name__.lower()

