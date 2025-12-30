"""
Dependency injection functions for FastAPI endpoints.
"""
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")


def get_db() -> Generator:
    """
    Get database session.
    
    Yields:
        Session: Database session
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> models.User:
    """
    Get current authenticated user from JWT token.
    
    Args:
        db: Database session
        token: JWT token from request
        
    Returns:
        models.User: Current user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """
    Get current active user.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        models.User: Current active user
        
    Raises:
        HTTPException: If user is inactive
    """
    if not crud.user.is_active(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_active_user),
) -> models.User:
    """
    Get current active superuser.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        models.User: Current active superuser
        
    Raises:
        HTTPException: If user is not a superuser
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user doesn't have enough privileges",
        )
    return current_user
