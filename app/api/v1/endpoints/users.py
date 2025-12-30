"""
User endpoints for CRUD operations.
"""
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve active users with pagination.
    
    Args:
        db: Database session
        skip: Number of users to skip
        limit: Maximum number of users to return
        current_user: Currently authenticated user
        
    Returns:
        List[schemas.User]: List of active users only
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    active_users = [user for user in users if crud.user.is_active(user)]
    return active_users


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    
    Args:
        db: Database session
        user_in: User creation data
        
    Returns:
        schemas.User: Created user
        
    Raises:
        HTTPException: If user with email or username already exists
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists.",
        )
    user = crud.user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    full_name: str = None,
    email: str = None,
    phone_number: str = None,
    avatar_url: str = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update current user's information.
    
    Args:
        db: Database session
        full_name: New full name
        email: New email
        phone_number: New phone number
        avatar_url: New avatar URL
        current_user: Currently authenticated user
        
    Returns:
        schemas.User: Updated user
    """
    current_user_data = schemas.UserUpdate(**current_user.__dict__)
    if full_name is not None:
        current_user_data.full_name = full_name
    if email is not None:
        current_user_data.email = email
    if phone_number is not None:
        current_user_data.phone_number = phone_number
    if avatar_url is not None:
        current_user_data.avatar_url = avatar_url
    user = crud.user.update(db, db_obj=current_user, obj_in=current_user_data)
    return user


@router.put("/me/password", response_model=schemas.User)
def update_user_password(
    *,
    db: Session = Depends(deps.get_db),
    password_data: schemas.user.UserPasswordUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update current user's password.
    
    Args:
        db: Database session
        password_data: Password update data with old and new passwords
        current_user: Currently authenticated user
        
    Returns:
        schemas.User: Updated user
        
    Raises:
        HTTPException: If old password is incorrect
    """
    try:
        user = crud.user.update_password(
            db, db_obj=current_user, password_data=password_data
        )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/me", response_model=schemas.User)
def read_user_me(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user's information.
    
    Args:
        current_user: Currently authenticated user
        
    Returns:
        schemas.User: Current user
    """
    return current_user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get user by ID.
    
    Args:
        user_id: User ID
        current_user: Currently authenticated user
        db: Database session
        
    Returns:
        schemas.User: User information
        
    Raises:
        HTTPException: If user not found
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user doesn't have enough privileges",
        )
    return user
