from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.core.config import settings
from app.api import deps
from typing import Optional
from app.models.user import User
from app.core.redis_conf import redis_client
from passlib.context import CryptContext

router = APIRouter()

@router.post("/register", response_model=Optional[schemas.UserRepresentation])
def register_user(user_data: schemas.UserCreateUpdate, db: Session = Depends(deps.get_db)):
    user = db.query(User).filter_by(email=user_data.email).first()

    if user and redis_client.get(f"verify_code{user.id}"):
        raise HTTPException(
            status_code=400, detail="Your verification code is already send"
        )

    elif not user:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash(user_data.password)

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            is_superuser=user_data.is_superuser,
            hashed_password=hashed_password,
            is_active=False
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    redis_client.setex(f"verify_code{user.id}", settings.CODE_EXPIRES_IN, user.id)
    return user

