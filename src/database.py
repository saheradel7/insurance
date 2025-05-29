from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from src.config.env import env


# DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:30018/postgres"
# DATABASE_URL = (
#             f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@"
#             f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
#         )
DATABASE_URL = (
    f"postgresql+psycopg2://{env.db_username}:{env.db_password}@"
    f"{env.db_host}:{env.db_port}/{env.db_name}?sslmode={env.db_sslmode}"
)
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_context = Annotated[Session, Depends(get_db)]
