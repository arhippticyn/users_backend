from fastapi import FastAPI, Depends, File, UploadFile, Form, HTTPException
from sqlalchemy.orm import Session
from models import UserBase
from db import get_db, User
import os
from PIL import Image
from datetime import datetime, date, timedelta
from passlib.hash import bcrypt

app = FastAPI()

UPLOAD_DIR = 'upload'
os.makedirs(UPLOAD_DIR, exist_ok=True)

def hash_password(password: str) -> str:
    # Обрезаем пароль до 72 байт, так как bcrypt поддерживает максимум 72
    truncated = password.encode('utf-8')[:72]
    # Возвращаем строку хэша
    return bcrypt.hash(truncated)


@app.post('/add')
async def add(username: str = Form(...),password: str = Form(...),date_born: str = Form(...),sex: str = Form(...),file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
     file_path = f'upload/{file.filename}'
     with open(file_path, 'wb') as f:
        f.write(await file.read())
    
     date_reg = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
     date_borns = datetime.strptime(date_born, '%Y-%m-%d').date()
     today = date.today()
     age = today.year - date_borns.year - ((today.month, today.day) < (date_borns.month, date_borns.day))
     user_db = User(username=username,password=hash_password(password), file=file.filename, date_reg=date_reg, date_born=date_borns, age=age, sex=sex)
     db.add(user_db)
     db.commit()
     db.refresh(user_db)
     return user_db
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/procces-image/{user_id}')
async def proccess_image(user_id: int,width_r: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user.file:
        return 'error'
    start = datetime.now()
    file_path = f'upload/{user.file}'
    img = Image.open(file_path)
    width, height = img.size
    height_r = int((width_r / width) * height)
    remake_img = img.resize((width_r,height_r)).rotate(20).convert("L")
    remake_path = f'upload/remake_{user.file}'
    remake_img.save(remake_path)
    end = datetime.now()
    return {'message': 'img is remake', 'old_weight': width, 'old_height': height, 'time_work': end - start}

@app.get('/users')
async def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get('/user/{user_id}', response_model=UserBase)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return user

@app.delete('/users/{user_id}')
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User with id={user_id} not found"
        )
    db.delete(user)
    db.commit()
    return {'message': f'User {user_id} is deleted'}