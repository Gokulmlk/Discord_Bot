from sqlmodel import SQLModel
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from . import models

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
def create_tables():
    SQLModel.metadata.create_all(engine)

def delete_tables():
    SQLModel.metadata.drop_all(engine)