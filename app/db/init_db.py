"""
Database initialization script.
"""
from sqlalchemy.orm import Session
from app.crud.crud_user import user
from app.schemas.user import UserCreate
from app.core.config import settings
from app.db import base  # noqa: F401


def init_db(db: Session) -> None:
    """
    Initialize database with initial data.
    
    Args:
        db: Database session
    """
    try:
        # Create initial superuser
        user_in = UserCreate(
            email="admin@example.com",
            username="admin",
            full_name="Initial Admin",
            password="admin123",
            is_superuser=True,
        )
        
        # Check if user already exists
        existing_user = user.get_by_email(db, email=user_in.email)
        if not existing_user:
            created_user = user.create(db, obj_in=user_in)
            print("✅ Initial admin user created successfully")
            print(f"   User ID: {created_user.id}")
            print(f"   Email: {created_user.email}")
            print(f"   Username: {created_user.username}")
        else:
            print("ℹ️  Initial admin user already exists")
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        print("   Make sure PostgreSQL is running and the database/schema are created.")
        print("   Run 'python setup_db.py' to set up the database first.")
        raise
