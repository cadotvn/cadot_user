"""
Authentication endpoints for user login.
"""
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps
from app.core import security

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.LoginResponse)
def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    
    Args:
        db: Database session
        form_data: OAuth2 password request form (username field can contain email or username)
        
    Returns:
        schemas.LoginResponse: Access token and user information
        
    Raises:
        HTTPException: If credentials are invalid or user is disabled
    """
    # OAuth2PasswordRequestForm uses 'username' field, but we accept email or username
    user = crud.user.authenticate_by_email_or_username(
        db, email_or_username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active (not disabled)
    if not crud.user.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled",
        )
    
    # Create access token
    access_token = security.create_access_token(subject=user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user,
    }


@router.post("/login", response_model=schemas.LoginResponse)
def login_with_json(
    *,
    db: Session = Depends(deps.get_db),
    login_data: schemas.LoginRequest,
) -> Any:
    """
    Login with email/username and password, get an access token and user information.
    
    Args:
        db: Database session
        login_data: Login request with email_or_username and password
        
    Returns:
        schemas.LoginResponse: Access token and user information
        
    Raises:
        HTTPException: If credentials are invalid or user is disabled
    """
    user = crud.user.authenticate_by_email_or_username(
        db,
        email_or_username=login_data.email_or_username,
        password=login_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active (not disabled)
    if not crud.user.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled",
        )
    
    # Create access token
    access_token = security.create_access_token(subject=user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user,
    }

