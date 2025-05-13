from dotenv import load_dotenv
import os
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, create_engine, Session as DBSession 
from sqlalchemy import Column, DateTime, func 
from sqlalchemy.sql import func
from datetime import datetime 

load_dotenv()

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    messages: List["Message"] = Relationship(back_populates="author")
    name: str

class Session(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()))
    messages: List["Message"] = Relationship(back_populates="session")

    channel_id: str
    is_dm: bool

    deleted: bool = Field(default=False)

class Message(SQLModel,table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    author: str
    text: str

    session_id: Optional[int] = Field(default=None, foreign_key="session.id")
    session: Optional[Session] = Relationship(back_populates="messages")

    author_id: Optional[int] = Field(default=None, foreign_key="user.id")
    author: Optional[User] = Relationship(back_populates="messages")  

database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url, echo=True)

# SQLModel.metadata.create_all(engine)

# with engine.connect() as session:
#     print(session)
database_session = DBSession(engine)

# Create
discord_channel1 = Session(channel_id="1234567890", is_dm=False)
discord_channel2 = Session(channel_id="0987654321", is_dm=True)

# add to the session
database_session.add(discord_channel1)
database_session.add(discord_channel2)
# commit the session
database_session.commit()