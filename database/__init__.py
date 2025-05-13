from sqlmodel import SQLModel
from .engine import engine
from . import models

def create_tables():
    SQLModel.metadata.create_all(engine)

def delete_tables():
    SQLModel.metadata.drop_all(engine)