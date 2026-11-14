from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import get_db
from schemas import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse,
    APIResponse
)
from services import auth_service
from services.exceptions import (
    UserAlreadyExistsError,
    InvalidCredentialsError
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register",response_model=APIResponse[UserResponse],status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: Session = Depends(get_db)):
    try:
        user = auth_service.register_user(db, data)

        return APIResponse(
            result=user,
            message="User registered successfully"
        )

    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )


@router.post("/login",response_model=APIResponse[TokenResponse])
def login(data: UserLogin, db: Session = Depends(get_db)):

    try:
        token = auth_service.authenticate_user(
            db,
            data.username,
            data.password
        )

        return APIResponse(
            result=TokenResponse(access_token=token),
            message="Login successful"
        )

    except InvalidCredentialsError:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )