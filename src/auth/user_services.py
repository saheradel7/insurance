import logging
from typing import Any
from fastapi import HTTPException, Depends
# from ..database import Database, get_db
from src.database import db_context

from .user_schema import UserCreate, UserRead, UserUpdate
from .user_repository import create_user, get_user_by_id, get_user_by_keycloak_id, update_user, delete_user, get_all_users
from sqlalchemy.orm import Session


# Creating a user
def create_user_service(user: UserCreate, db: db_context) -> UserRead:
    """
    Create a new user via the repository, then fetch and return it.
    """
    try:
        # Create the user and get its new ID
        user_id = create_user(user, db)
        return get_user_by_id(user_id, db)
    except HTTPException as e:
        raise e
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"User creation failed: {error}")
    
    
# Get all users
def get_all_users_service(db: db_context) -> list[UserRead]:
    """
    Get all users
    """
    try:
        return get_all_users(db)
    except HTTPException as e:
        raise e
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {error}")
    
    
# Retrieve a user by id
def get_user_by_id_service(user_id: int, db: db_context) -> UserRead:
    """
    Fetch a user by ID via the repository.
    """
    try:
        user = get_user_by_id(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException as e:
        raise e
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {error}")
    
    
# Retrieve a user by keycloak id
def get_user_by_keycloak_id_service(user_keycloak_id: str, db: db_context) -> UserRead:
    """
    Fetch a user by keycloak ID via the repository.
    """
    try:
        user = get_user_by_keycloak_id(user_keycloak_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException as e:
        raise e
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {error}")
    
    
# Update a user by keycloak id
def update_user_service(user_keycloak_id: str, user: UserUpdate, db: db_context) -> UserRead:
    """
    Update a user by keycloak ID via the repository.
    """
    try:
        return update_user(user_keycloak_id, user, db)
    except HTTPException as e:
        raise e
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {error}")
    
    
# Delete a user by keycloak id
def delete_user_service(user_keycloak_id: str, db: db_context):
    """
    Delete a user by keycloak ID via the repository.
    """
    try:
        delete_user(user_keycloak_id, db)
    except HTTPException as e:
        raise e
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {error}")
    
    
