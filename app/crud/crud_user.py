"""
User-specific CRUD operations.
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserPasswordUpdate
from app.core.security import get_password_hash, verify_password


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """
    CRUD operations for User model.
    
    Extends the base CRUD class with user-specific functionality.
    """
    
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """
        Get user by email address.
        
        Args:
            db: Database session
            email: User's email address
            
        Returns:
            Optional[User]: Found user or None
        """
        return db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """
        Get user by username.
        
        Args:
            db: Database session
            username: User's username
            
        Returns:
            Optional[User]: Found user or None
        """
        return db.query(User).filter(User.username == username).first()
    
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """
        Create new user with hashed password.
        
        Args:
            db: Database session
            obj_in: User creation data
            
        Returns:
            User: Created user
        """
        # Set default status to active if not provided
        is_active = getattr(obj_in, 'is_active', True)
        is_superuser = getattr(obj_in, 'is_superuser', False)
        
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            full_name=obj_in.full_name,
            phone_number=obj_in.phone_number,
            avatar_url=obj_in.avatar_url,
            hashed_password=get_password_hash(obj_in.password),
            is_active=is_active,
            is_superuser=is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, db: Session, *, db_obj: User, obj_in: UserUpdate
    ) -> User:
        """
        Update user information.
        
        Args:
            db: Database session
            db_obj: Database user object
            obj_in: Update data
            
        Returns:
            User: Updated user
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password.
        
        Args:
            db: Database session
            email: User's email address
            password: Plain text password
            
        Returns:
            Optional[User]: Authenticated user or None
        """
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def is_active(self, user: User) -> bool:
        """
        Check if user is active.
        
        Args:
            user: User object
            
        Returns:
            bool: True if user is active
        """
        return user.is_active
    
    def is_superuser(self, user: User) -> bool:
        """
        Check if user is a superuser.
        
        Args:
            user: User object
            
        Returns:
            bool: True if user is a superuser
        """
        return user.is_superuser
    
    def update_password(
        self, db: Session, *, db_obj: User, password_data: UserPasswordUpdate
    ) -> User:
        """
        Update user password with old password verification.
        
        Args:
            db: Database session
            db_obj: Database user object
            password_data: Password update data with old and new passwords
            
        Returns:
            User: Updated user
            
        Raises:
            ValueError: If old password is incorrect
        """
        # Verify old password
        if not verify_password(password_data.old_password, db_obj.hashed_password):
            raise ValueError("Old password is incorrect")
        
        # Update with new hashed password
        db_obj.hashed_password = get_password_hash(password_data.new_password)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


user = CRUDUser(User)
