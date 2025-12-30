"""
User schemas for request/response validation.
"""
from typing import Optional, Union
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator


class UserBase(BaseModel):
    """Base user schema with common fields."""
    
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    """Schema for creating a new user."""
    
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class UserInDBBase(UserBase):
    """Base user schema for database operations."""
    
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @validator('created_at', 'updated_at', pre=True)
    def parse_datetime(cls, v):
        """Parse datetime fields from various input types."""
        if v is None:
            return None
        if isinstance(v, datetime):
            return v
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                return None
        return v
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
        validate_assignment = True
        arbitrary_types_allowed = True


class User(UserInDBBase):
    """Schema for user responses (excluding sensitive data)."""
    pass


class UserInDB(UserInDBBase):
    """Schema for user in database (including hashed password)."""
    
    hashed_password: str


class UserPasswordUpdate(BaseModel):
    """Schema for updating user password."""
    
    old_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)
