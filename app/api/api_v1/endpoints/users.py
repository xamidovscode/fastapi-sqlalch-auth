from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps

from typing import List

router = APIRouter()

@router.post("/create", response_model=schemas.UserRead)
def register_user(
    user_data: schemas.UserCreate, db: Session = Depends(deps.get_db),
):
    db_user = crud.user.get(db, email=user_data.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.user.create(db=db, user_data=user_data)


@router.get("/users", response_model=List[schemas.UserRead])
def register_user(db: Session = Depends(deps.get_db)):
    return crud.user.get_multi(db=db, skip=0, limit=100)


@router.get("/users/{user_id}", response_model=schemas.UserRead)
def register_user(user_id: int, db: Session = Depends(deps.get_db)):
    return crud.user.get(db=db, obj_id=user_id)


@router.delete("/users/{user_id}", response_model=schemas.UserRead)
def register_user(user_id: int, db: Session = Depends(deps.get_db)):
    return crud.user.remove(db=db, obj_id=user_id)