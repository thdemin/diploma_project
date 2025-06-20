from fastapi import FastAPI, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from app.database import SessionLocal
from app import schemas, crud
from app.ml import get_ml_response, load_model   
from app.auth import authenticate_user

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"msg": "Hello from Marketing Bot backend!"}


@app.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)


@app.post("/login", response_model=schemas.UserOut)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return db_user


@app.post("/requests", response_model=schemas.RequestOut)
def create_request(request: schemas.RequestCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_request(db, request, user_id)


@app.get("/requests", response_model=list[schemas.RequestOut])
def get_requests(user_id: int = None, db: Session = Depends(get_db)):
    return crud.get_requests(db, user_id)


@app.patch("/requests/{request_id}/status", response_model=schemas.RequestOut)
def update_request_status(request_id: int, status: str, db: Session = Depends(get_db)):
    updated = crud.update_request_status(db, request_id, new_status=status)
    if not updated:
        raise HTTPException(status_code=404, detail="Request not found")
    return updated


@app.post("/campaigns", response_model=schemas.CampaignOut)
def create_campaign(campaign: schemas.CampaignCreate, db: Session = Depends(get_db)):
    return crud.create_campaign(db, campaign)


@app.get("/campaigns", response_model=list[schemas.CampaignOut])
def get_campaigns(db: Session = Depends(get_db)):
    return crud.get_campaigns(db)


@app.post("/chat", response_model=schemas.ChatMessageOut)
def send_message(message: schemas.ChatMessageCreate, db: Session = Depends(get_db)):
    return crud.create_chat_message(db, message)


@app.get("/chat", response_model=list[schemas.ChatMessageOut])
def get_chat_history(
    user_id: int = Query(None),
    request_id: int = Query(None),
    db: Session = Depends(get_db)
):
    """
    История чата:
    - Можно указать user_id (все сообщения пользователя)
    - request_id (все сообщения по заявке)
    - или оба параметра одновременно
    """
    return crud.get_chat_history(db, user_id=user_id, request_id=request_id)


@app.get("/faq", response_model=list[schemas.FAQOut])
def get_faq(db: Session = Depends(get_db)):
    return crud.get_all_faq(db)


@app.post("/mlchat")
async def mlchat(request: Request):
    import app.ml as ml
    data = await request.json()
    user_message = data.get("text") or data.get("message")
    if not user_message:
        return {"response": "Пусте повідомлення", "intent": "empty"}
    ml.load_model()
    intent = ml.pipeline.predict([user_message])[0]
    resp_list = ml.responses.get(intent, [])
    response = resp_list[0] if resp_list else "Вибачте, я не зрозумів запитання. Спробуйте інакше!"
    return {"response": response, "intent": intent}
