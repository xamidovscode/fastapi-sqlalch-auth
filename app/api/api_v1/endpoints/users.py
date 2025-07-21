from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.post("/register", response_model=schemas.UserRead)
def register_user(
    user_data: schemas.UserCreate, db: Session = Depends(deps.get_db),
):
    db_user = crud.user.get(db, email=user_data.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.user.create(db=db, user_data=user_data)
