"""
Configuration settings for the application.
"""
from typing import List, Union, Optional
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    PROJECT_NAME: str = "User Management API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database - All database settings must come from .env file
    DATABASE_URL: Optional[str] = None  # Can be provided directly in .env
    DATABASE_HOST: Optional[str] = None  # Required if DATABASE_URL not provided
    DATABASE_PORT: Optional[int] = None  # Optional, defaults to 5432
    DATABASE_NAME: Optional[str] = None  # Required if DATABASE_URL not provided
    DATABASE_USER: Optional[str] = None  # Required if DATABASE_URL not provided
    DATABASE_PASSWORD: Optional[str] = None  # Required if DATABASE_URL not provided
    DATABASE_SCHEMA: str = "cadot"  # Default schema, can be overridden in .env
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Assemble CORS origins."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    @validator("DATABASE_URL", pre=True, always=True)
    def assemble_database_url(cls, v: str, values: dict) -> str:
        """Assemble database URL from individual components."""
        # If DATABASE_URL is provided directly, use it and append schema
        if v:
            schema = values.get("DATABASE_SCHEMA", "cadot")
            if "?options=-csearch_path%3D" not in v:
                return f"{v}?options=-csearch_path%3D{schema}"
            return v
        
        # Otherwise, construct from individual components
        host = values.get("DATABASE_HOST")
        port = values.get("DATABASE_PORT")
        name = values.get("DATABASE_NAME")
        user = values.get("DATABASE_USER")
        password = values.get("DATABASE_PASSWORD")
        schema = values.get("DATABASE_SCHEMA", "cadot")
        
        # Check if all required components are provided
        if not all([host, name, user, password]):
            raise ValueError(
                "Database configuration incomplete. Please provide either DATABASE_URL "
                "or all of: DATABASE_HOST, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD "
                "in your .env file"
            )
        
        # Construct the database URL with schema
        port_str = f":{port}" if port else ""
        return f"postgresql://{user}:{password}@{host}{port_str}/{name}?options=-csearch_path%3D{schema}"
    
    # Email settings (for future use)
    SMTP_TLS: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: str = ""
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
