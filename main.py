from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import User
from schemas import UserCreate, UserUpdate, UserResponse
from typing import List

Base.metadata.create_all(bind=engine)
app=FastAPI()


@app.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/users/{user_id}", response_model=UserResponse)
def get_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User wasn't found")
    return user

@app.post("/users/", response_model=UserResponse)
def create_user(user:UserCreate, db: Session = Depends(get_db)):
    existing=db.query(User).filter(User.email==user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user=User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id:int, user:UserUpdate, db: Session = Depends(get_db)):
    db_user=db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User wasn't found")

    for key, value in user.dict().items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

@app.patch("/users/{user_id}", response_model=UserResponse)
def partial_update_user(user_id:int, user:UserUpdate, db: Session = Depends(get_db)):
    db_user=db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User wasn't found")

    for key, value in user.dict(exclude_none=True).items():
        setattr(db_user, key, value)


    db.commit()
    db.refresh(db_user)
    return db_user



@app.delete("/users/{user_id}")
def delete_user(user_id:int, db: Session = Depends(get_db)):
    db_user=db.query(User).filter(User.id==user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User wasn't found")

    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}





