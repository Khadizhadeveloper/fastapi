from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import User
from typing import List
from auth import hash_password, verify_password, create_token, get_current_user
from schemas import TokenResponse, LoginRequest, UserResponse, UserCreate, UserUpdate

Base.metadata.create_all(bind=engine)
app=FastAPI()


@app.post("/auth/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing=db.query(User).filter(User.email==user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user.name,
        email=user.email,
        age=user.age,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/auth/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user=db.query(User).filter(User.email==data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password or email")

    token=create_token({"sub": user.email})
    return {"access_token": token}




@app.get("/users/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/users/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(User).all()

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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





