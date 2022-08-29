from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db_database import Base


class file_data(Base):
    __tablename__ = "textFiles"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    length = Column(Integer)
    user_id = Column(String, ForeignKey("users.uuid"))
    creator = relationship("User", back_populates="textFiles")


class keywords(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    list_keywords = Column(String)
    user_id = Column(String, ForeignKey("users.uuid"))
    creator = relationship("User", back_populates="keywords")


class User(Base):
    __tablename__ = "users"

    uuid = Column(String, primary_key=True, index=True)
    username = Column(String)

    textFiles = relationship("file_data", back_populates="creator")
    keywords = relationship("keywords", back_populates="creator")
