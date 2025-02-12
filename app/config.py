from pydantic_settings import BaseSettings
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv

# Todo add modifications as per the working env
load_dotenv(".env", override=True)


class Settings(BaseSettings):
    '''
        Settings class to set the environment variables
    '''
    database_url: str
    otp_expiry_time: int = 5
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str

    # UPLOAD_FOLDER: str = "uploads/"
    # ALLOWED_EXTENSIONS: set = {"pdf", "jpg", "jpeg", "png"}

    class Config:
        env_file = ".env"


settings = Settings()


# Setting up database
DATABASE_URL = settings.database_url


engine = create_engine(
    # Todo check other parameters
    DATABASE_URL
)

print("Connection to DB established. Database URL: ", DATABASE_URL)

# Creating DB session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Creating Base for models
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

