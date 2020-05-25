from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    TEXT,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    tweet = relationship("Tweet", back_populates="author")


class Tweet(Base):
    __tablename__ = "tweets"
    id = Column(BigInteger, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    message = Column(TEXT)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    author = relationship("User", back_populates="tweet")


class Following(Base):
    __tablename__ = "following"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    follows_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
