"""
Main API router for v1 endpoints.
"""
from fastapi import APIRouter
from app.api.v1.endpoints import users, auth

api_router = APIRouter()

# Include authentication endpoints
api_router.include_router(auth.router, tags=["authentication"])

# Include user endpoints
api_router.include_router(users.router, prefix="/users", tags=["users"])
