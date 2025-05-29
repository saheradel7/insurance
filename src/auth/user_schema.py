from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    firstname: str
    lastname: str
    email: str
    role: str
    keycloak_user_id: str
    
class UserUpdate(BaseModel):
    firstname: str
    lastname: str
    role: str


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    firstname: str
    lastname: str
    role: str
    keycloak_user_id: str

    class Config:
        orm_mode = True
        
class UserSignIn(BaseModel):
    username: str
    password: str
