"""
Base CRUD class with common database operations.
"""
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base CRUD class with common database operations.
    
    Generic types:
        ModelType: SQLAlchemy model class
        CreateSchemaType: Pydantic create schema
        UpdateSchemaType: Pydantic update schema
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        Initialize CRUD object with model.
        
        Args:
            model: SQLAlchemy model class
        """
        self.model = model
    
    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Get object by ID.
        
        Args:
            db: Database session
            id: Object ID
            
        Returns:
            Optional[ModelType]: Found object or None
        """
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Get multiple objects with pagination.
        
        Args:
            db: Database session
            skip: Number of objects to skip
            limit: Maximum number of objects to return
            
        Returns:
            List[ModelType]: List of objects
        """
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create new object.
        
        Args:
            db: Database session
            obj_in: Object data
            
        Returns:
            ModelType: Created object
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Update object.
        
        Args:
            db: Database session
            db_obj: Database object to update
            obj_in: Update data
            
        Returns:
            ModelType: Updated object
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove(self, db: Session, *, id: int) -> ModelType:
        """
        Delete object by ID.
        
        Args:
            db: Database session
            id: Object ID
            
        Returns:
            ModelType: Deleted object
        """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
