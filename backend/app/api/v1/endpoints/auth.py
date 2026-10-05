from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings

router = APIRouter()


@router.post(
    "/register",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_in: schemas.UserCreate,
    db: Session = Depends(deps.get_db),
):
    existing_username = (
        db.query(models.User)
        .filter(models.User.username == user_in.username)
        .first()
    )

    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username already exists.",
        )

    existing_email = (
        db.query(models.User)
        .filter(models.User.email == str(user_in.email))
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists.",
        )

    db_user = models.User(
        username=user_in.username.strip(),
        email=str(user_in.email).lower(),
        hashed_password=security.get_password_hash(
            user_in.password
        ),
        role=user_in.role or "developer",
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post(
    "/login/access-token",
    response_model=schemas.Token,
)
@router.post(
    "/login",
    response_model=schemas.Token,
    include_in_schema=False,
)
def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(deps.get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.username == form_data.username)
        .first()
    )

    if not user or not security.verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = security.create_access_token(
        subject=user.username,
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }