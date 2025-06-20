from sqlalchemy.orm import Session
from . import models, schemas
from passlib.hash import bcrypt
from datetime import datetime


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        role="client"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_request(db: Session, request: schemas.RequestCreate, user_id: int):
    db_request = models.Request(
        user_id=user_id,
        title=request.title,
        description=request.description,
        type=request.type
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def get_requests(db: Session, user_id: int = None):
    if user_id:
        return db.query(models.Request).filter(models.Request.user_id == user_id).all()
    return db.query(models.Request).all()

def get_request_by_id(db: Session, request_id: int):
    return db.query(models.Request).filter(models.Request.id == request_id).first()

def update_request_status(db: Session, request_id: int, new_status: str):
    request = get_request_by_id(db, request_id)
    if request:
        request.status = new_status
        request.updated_at = datetime.now()
        db.commit()
        db.refresh(request)
    return request


def create_campaign(db: Session, campaign: schemas.CampaignCreate):
    db_campaign = models.Campaign(
        request_id=campaign.request_id,
        name=campaign.name,
        channel=campaign.channel,
        budget=campaign.budget,
        start_date=campaign.start_date,
        end_date=campaign.end_date
    )
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

def get_campaigns(db: Session):
    return db.query(models.Campaign).all()



def create_chat_message(db: Session, message: schemas.ChatMessageCreate):
    db_message = models.ChatHistory(
        user_id=message.user_id,
        message=message.message,
        sender=message.sender,
        request_id=message.request_id    
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_chat_history(db: Session, user_id: int = None, request_id: int = None):
    """
    получаем историю чата по заявке (или всем заявкам пользователя)
    """
    query = db.query(models.ChatHistory)
    if user_id:
        query = query.filter(models.ChatHistory.user_id == user_id)
    if request_id:
        query = query.filter(models.ChatHistory.request_id == request_id)
    return query.order_by(models.ChatHistory.created_at.asc()).all()


def get_all_faq(db: Session):
    return db.query(models.FAQ).all()
