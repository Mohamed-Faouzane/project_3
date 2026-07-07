from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

import models
import schemas
import auth
from database import get_db

router = APIRouter(prefix = "/users", tags = ["users"])

@router.post("/register", response_model = schemas.UserResponse, status_code = 201)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
   
    # Check if email already exists
    existing_email = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code = 400, detail = "Email already registered")
    
    # Check if username already exists
    existing_username = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code = 400, detail = "Username already taken")
    
    # Hash password and create user
    hashed_password = auth.hash_password(user.password)
    new_user = models.User(
        email = user.email,
        username = user.username,
        hashed_password = hashed_password
    )
    db.add(new_user)        # stages the new user
    db.commit()             # writes it to the database permanently 
    db.refresh(new_user)    #  reloads the object from the database so id and created_at are populated (the DB generates these, the Python object doesn't know them until refreshed)
    return new_user

@router.post("/login", response_model = schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid credentials",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    # Create and return JWT token
    access_token = auth.create_access_token(
        data = {"sub": user.username},
        expires_delta = timedelta(minutes = auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}