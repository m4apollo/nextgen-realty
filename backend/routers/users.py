from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from backend.db import get_sync_session
from backend.models import User, UserCreate, UserRead
from backend.utils.security impor get_password_hash, create_access_token, get_current_user
from utils.logging import logger

router = APIRouter(tags=["Users"])

@router.post("/signup", response_model=UserRead)
async def create_user(user: UserCreate, session: Session = Depends(get_sync_session)):
    existing_user = session.exec(User.select().where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        company=user.company or "NextGen Realty"
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    logger.info(f"New user created: {user.email}")
    return db_user

@router.post("/login")
async def login(user: UserLogin, session: Session = Depends(get_sync_session)):
    db_user = session.exec(User.select().where(User.email == user.email)).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user