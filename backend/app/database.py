from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ДАННЫЕ ДЛЯ ПОДКЛЮЧЕНИЯ К MySQL
DB_USER = "root"         # свой username
DB_PASS = "Artem202020"     # свой пароль
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "marketing_bot_db"

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
