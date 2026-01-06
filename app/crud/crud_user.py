"""
User-specific CRUD operations.
"""

from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserPasswordUpdate
from app.core.security import get_password_hash, verify_password
from app.core.logger import get_logger

logger = get_logger(__name__)


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
        logger.info(f"get_by_email called with email={email}")
        try:
            user = db.query(User).filter(User.email == email).first()
            if user:
                logger.info(
                    f"get_by_email: User found with email={email}, user_id={user.id}"
                )
            else:
                logger.info(f"get_by_email: No user found with email={email}")
            return user
        except Exception as exception:
            logger.error(
                f"get_by_email failed: email={email}, error={str(exception)}", exc_info=True
            )
            raise

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """
        Get user by username.

        Args:
            db: Database session
            username: User's username

        Returns:
            Optional[User]: Found user or None
        """
        logger.info(f"get_by_username called with username={username}")
        try:
            user = db.query(User).filter(User.username == username).first()
            if user:
                logger.info(
                    f"get_by_username: User found with username={username}, user_id={user.id}"
                )
            else:
                logger.info(f"get_by_username: No user found with username={username}")
            return user
        except Exception as exception:
            logger.error(
                f"get_by_username failed: username={username}, error={str(exception)}",
                exc_info=True,
            )
            raise

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """
        Create new user with hashed password.

        Args:
            db: Database session
            obj_in: User creation data

        Returns:
            User: Created user
        """
        logger.info(
            f"create called with email={obj_in.email}, username={obj_in.username}"
        )
        try:
            # Set default status to active if not provided
            user_is_active = getattr(obj_in, "is_active", True)
            user_is_superuser = getattr(obj_in, "is_superuser", False)

            new_user = User(
                email=obj_in.email,
                username=obj_in.username,
                full_name=obj_in.full_name,
                phone_number=obj_in.phone_number,
                avatar_url=obj_in.avatar_url,
                hashed_password=get_password_hash(obj_in.password),
                is_active=user_is_active,
                is_superuser=user_is_superuser,
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            logger.info(
                f"create: User created successfully with email={obj_in.email}, username={obj_in.username}, user_id={new_user.id}, is_active={user_is_active}, is_superuser={user_is_superuser}"
            )
            return new_user
        except Exception as exception:
            logger.error(
                f"create failed: email={obj_in.email}, username={obj_in.username}, error={str(exception)}",
                exc_info=True,
            )
            db.rollback()
            raise

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        """
        Update user information.

        Args:
            db: Database session
            db_obj: Database user object
            obj_in: Update data

        Returns:
            User: Updated user
        """
        logger.info(f"update called with user_id={db_obj.id}, email={db_obj.email}")
        try:
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)

            logger.info(
                f"update: Updating fields={list(update_data.keys())} for user_id={db_obj.id}"
            )
            updated_user = super().update(db, db_obj=db_obj, obj_in=update_data)
            logger.info(f"update: User updated successfully with user_id={db_obj.id}")
            return updated_user
        except Exception as exception:
            logger.error(
                f"update failed: user_id={db_obj.id}, error={str(exception)}", exc_info=True
            )
            raise

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
        logger.info(f"authenticate called with email={email}")
        try:
            user = self.get_by_email(db, email=email)
            if not user:
                logger.warning(f"authenticate: User not found with email={email}")
                return None
            if not verify_password(password, user.hashed_password):
                logger.warning(
                    f"authenticate: Password verification failed for email={email}, user_id={user.id}"
                )
                return None
            logger.info(
                f"authenticate: User authenticated successfully with email={email}, user_id={user.id}"
            )
            return user
        except Exception as exception:
            logger.error(
                f"authenticate failed: email={email}, error={str(exception)}", exc_info=True
            )
            raise

    def authenticate_by_email_or_username(
        self, db: Session, *, email_or_username: str, password: str
    ) -> Optional[User]:
        """
        Authenticate user with email or username and password.

        Args:
            db: Database session
            email_or_username: User's email address or username
            password: Plain text password

        Returns:
            Optional[User]: Authenticated user or None
        """
        logger.info(
            f"authenticate_by_email_or_username called with email_or_username={email_or_username}"
        )
        try:
            # Try to find user by email first
            user = self.get_by_email(db, email=email_or_username)
            if not user:
                # If not found by email, try username
                user = self.get_by_username(db, username=email_or_username)
            
            if not user:
                logger.warning(
                    f"authenticate_by_email_or_username: User not found with email_or_username={email_or_username}"
                )
                return None
            
            if not verify_password(password, user.hashed_password):
                logger.warning(
                    f"authenticate_by_email_or_username: Password verification failed for email_or_username={email_or_username}, user_id={user.id}"
                )
                return None
            
            logger.info(
                f"authenticate_by_email_or_username: User authenticated successfully with email_or_username={email_or_username}, user_id={user.id}"
            )
            return user
        except Exception as exception:
            logger.error(
                f"authenticate_by_email_or_username failed: email_or_username={email_or_username}, error={str(exception)}",
                exc_info=True,
            )
            raise

    def is_active(self, user: User) -> bool:
        """
        Check if user is active.

        Args:
            user: User object

        Returns:
            bool: True if user is active
        """
        logger.info(f"is_active called with user_id={user.id}, email={user.email}")
        try:
            user_active_status = user.is_active
            logger.info(f"is_active: user_id={user.id}, is_active={user_active_status}")
            return user_active_status
        except Exception as exception:
            logger.error(
                f"is_active failed: user_id={user.id}, error={str(exception)}",
                exc_info=True,
            )
            raise

    def is_superuser(self, user: User) -> bool:
        """
        Check if user is a superuser.

        Args:
            user: User object

        Returns:
            bool: True if user is a superuser
        """
        logger.info(f"is_superuser called with user_id={user.id}, email={user.email}")
        try:
            user_superuser_status = user.is_superuser
            logger.info(
                f"is_superuser: user_id={user.id}, is_superuser={user_superuser_status}"
            )
            return user_superuser_status
        except Exception as exception:
            logger.error(
                f"is_superuser failed: user_id={user.id}, error={str(exception)}",
                exc_info=True,
            )
            raise

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
        logger.info(
            f"update_password called with user_id={db_obj.id}, email={db_obj.email}"
        )
        try:
            # Verify old password
            if not verify_password(password_data.old_password, db_obj.hashed_password):
                logger.warning(
                    f"update_password: Old password verification failed for user_id={db_obj.id}, email={db_obj.email}"
                )
                raise ValueError("Old password is incorrect")

            # Update with new hashed password
            db_obj.hashed_password = get_password_hash(password_data.new_password)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            logger.info(
                f"update_password: Password updated successfully for user_id={db_obj.id}, email={db_obj.email}"
            )
            return db_obj
        except ValueError:
            logger.error(
                f"update_password: ValueError raised for user_id={db_obj.id}, email={db_obj.email}"
            )
            raise
        except Exception as exception:
            logger.error(
                f"update_password failed: user_id={db_obj.id}, email={db_obj.email}, error={str(exception)}",
                exc_info=True,
            )
            db.rollback()
            raise


user = CRUDUser(User)
