from sqlalchemy import Column, Integer, String, Enum, Text, Date, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum('client', 'manager', 'admin'), default='client')
    created_at = Column(TIMESTAMP, server_default=func.now())

    requests = relationship("Request", back_populates="user")
    messages = relationship("ChatHistory", back_populates="user")

class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(Enum('new', 'in_progress', 'done', 'rejected'), default='new')
    type = Column(Enum('campaign', 'question', 'support', 'other'), default='campaign')
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="requests")
    campaigns = relationship("Campaign", back_populates="request")
    messages = relationship("ChatHistory", back_populates="request")  

class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id"))
    name = Column(String(255), nullable=False)
    channel = Column(Enum('facebook', 'instagram', 'google', 'other'), default='other')
    budget = Column(DECIMAL(12, 2))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(Enum('planned', 'active', 'completed', 'paused'), default='planned')
    created_at = Column(TIMESTAMP, server_default=func.now())

    request = relationship("Request", back_populates="campaigns")

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text, nullable=False)
    sender = Column(Enum('user', 'bot', 'manager'), default='user')
    created_at = Column(TIMESTAMP, server_default=func.now())
    request_id = Column(Integer, ForeignKey("requests.id"), nullable=True)  

    user = relationship("User", back_populates="messages")
    request = relationship("Request", back_populates="messages")  

class FAQ(Base):
    __tablename__ = "faq"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(255), nullable=False)
    answer = Column(Text, nullable=False)
