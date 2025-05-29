import logging
from sqlalchemy.orm import Session
from .user_model import User
from .user_schema import UserCreate, UserRead, UserUpdate
from fastapi import HTTPException, Depends
# from ..database import Database, get_db
from src.database import db_context


def create_user(user_in: UserCreate, db: db_context) -> int:
    """
    Create a new User row if none exists with the same keycloak_user_id.
    Returns the new user's .id on success.
    Raises CustomError on duplicate or other failures.
    """
    # check if the user exists in Keycloak
    if db.query(User).filter(User.keycloak_user_id == user_in.keycloak_user_id).first():
        print("User already exists in Keycloak and is already verified.")
        raise HTTPException(400, detail="Account is already verified.")

    # check if the user exists with same email
    if db.query(User).filter(User.email == user_in.email).first():
        print("User already exists with this email.")
        raise HTTPException(
            400, detail="User with this email already exists."
        )

    # check if the user exists with same username
    if db.query(User).filter(User.username == user_in.username).first():
        print("User already exists with this username.")
        raise HTTPException(
            400, detail="User with this username already exists."
        )
        
    print("User does not exist in Keycloak, creating a new user.")
    try:
        user = User(
            email=user_in.email,
            username=user_in.username,
            firstname=user_in.firstname,
            lastname=user_in.lastname,
            role=user_in.role,
            keycloak_user_id=user_in.keycloak_user_id,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user.id

    except Exception as err:
        print("Error in create_user")
        # otherwise fall back
        raise HTTPException(status_code=500, detail="Invalid data")
    
    
def get_all_users(db: db_context) -> list[UserRead]:
    """
    Fetch all users from the database.
    Returns a list of UserRead objects.
    Raises CustomError if any error occurs.
    """
    try:
        users = db.query(User).all()
        return users

    except Exception as err:
        print("Error in get_all_users")
        raise HTTPException(status_code=500, detail="Failed to fetch users")


def get_user_by_id(user_id: int, db: db_context) -> UserRead:
    """
    Fetch a User by its primary key.
    Raises CustomError if not found or other error happens.
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        return user
    
    except HTTPException as e:
        raise e
    except Exception as err:
        print("Error in get_user_by_id")
        raise HTTPException(status_code=500, detail="User fetch error: unknown")


def get_user_by_keycloak_id(
    keycloak_user_id: str, db: db_context
) -> UserRead:
    """
    Fetch a User by its keycloak_user_id.
    Raises CustomError if not found or other error happens.
    """
    try:
        user = db.query(User).filter(User.keycloak_user_id == keycloak_user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        return user

    except HTTPException as e:
        raise e
    except Exception as err:
        print(f"Error in get_user_by_keycloak_id: {err}")
        raise HTTPException(status_code=400, detail="Failed to fetch user" )


def update_user(
    keycloak_user_id: str, user_in: UserUpdate, db: db_context
) -> UserRead:
    """
    Edit a User by its keycloak key.
    Raises CustomError if not found or other error happens.
    """
    try:
        user = get_user_by_keycloak_id(keycloak_user_id, db)
        # Update the user fields
        user.firstname = user_in.firstname
        user.lastname = user_in.lastname
        user.role = user_in.role

        db.commit()
        db.refresh(user)
        return user

    except HTTPException as e:
        raise e
    except Exception as err:
        print("Error in edit_user")
        raise HTTPException(status_code=500, detail="User update error")
    
    
def delete_user(keycloak_user_id: str, db: db_context) -> None:
    """
    Delete a user by its keycloak_user_id.
    Raises CustomError if not found or other error happens.
    """
    try:
        user = get_user_by_keycloak_id(keycloak_user_id, db)

        db.delete(user)
        db.commit()
        
    except HTTPException as e:
        raise e
    except Exception as err:
        print("Error in delete_user")
        raise HTTPException(status_code=500, detail="User deletion error")
    

