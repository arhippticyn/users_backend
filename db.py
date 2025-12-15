from sqlalchemy import create_engine, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, Mapped, mapped_column
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)

Session_local = sessionmaker(engine)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    file: Mapped[str | None] = mapped_column(String(200))
    date_reg: Mapped[str] = mapped_column()
    date_born: Mapped[str] = mapped_column()
    age: Mapped[int] = mapped_column()
    password: Mapped[str] = mapped_column()
    sex: Mapped[str | None] = mapped_column() 
    
def get_db():
    db = Session_local()
    try:
        yield db
    finally:
        db.close()
             