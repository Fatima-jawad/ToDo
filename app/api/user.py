from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import schemas, models, security, cruds
from app.api.dependencies import get_db

user_router = APIRouter()


@user_router.post("/register/")
async def register(user: schemas.CreateUser, db: Session = Depends(get_db)):
    try:
        user = cruds.create_user(db=db, user=user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"email": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post("/login", response_model=schemas.Token)
async def login_for_access_token(user: schemas.Login, db: Session = Depends(get_db)):
    try:
        user = security.authenticate_user(db, user.email, user.password)
    except (HTTPException, Exception) as e:
        raise e
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"email": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post("/change_password")
async def change_password(
    info: schemas.ChangePassword,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    new_hashed_password = security.change_password(
        info.old_password, info.new_password, info.new_password2, current_user.password
    )
    db_obj = db.query(models.User).filter(models.User.id == current_user.id).first()
    db_obj.password = new_hashed_password
    db.commit()
    return {"message": "Password changed successfully"}
