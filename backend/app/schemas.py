from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date



class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):  
    email: EmailStr
    password: str

class UserOut(UserBase):
    id: int
    role: str
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True



class RequestBase(BaseModel):
    title: str
    description: Optional[str] = None
    type: Optional[str] = "campaign"

class RequestCreate(RequestBase):
    pass

class RequestOut(RequestBase):
    id: int
    user_id: int
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True



class CampaignBase(BaseModel):
    name: str
    channel: Optional[str] = "other"
    budget: Optional[float] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class CampaignCreate(CampaignBase):
    request_id: int

class CampaignOut(CampaignBase):
    id: int
    request_id: int
    status: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True



class ChatMessageBase(BaseModel):
    message: str
    sender: Optional[str] = "user"
    request_id: Optional[int] = None   

class ChatMessageCreate(ChatMessageBase):
    user_id: int

class ChatMessageOut(ChatMessageBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True



class FAQBase(BaseModel):
    question: str
    answer: str

class FAQOut(FAQBase):
    id: int

    class Config:
        orm_mode = True
