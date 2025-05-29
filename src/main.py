from fastapi import FastAPI
from src.property.apis import PropertyRouter
from src.auth.user_controller import user_router
from src.config.env import env

app = FastAPI()

app.include_router(PropertyRouter)
app.include_router(user_router)
