from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    user_type = Column(String, default="USER") # USER, ADMIN
    date_joined = Column(DateTime, default=datetime.utcnow)

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    filename = Column(String)
    file_path = Column(String)
    description = Column(String, nullable=True)
    release_date = Column(String, nullable=True)
    poster_url = Column(String, nullable=True)
    backdrop_url = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    rating = Column(Integer, nullable=True)
    last_watched = Column(DateTime, nullable=True)
    progress = Column(Integer, default=0) # Progress in seconds
