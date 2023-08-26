import os
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseSettings
load_dotenv(find_dotenv())                                        


# API_V1_STR: str = "/api/v1"
# SECRET_KEY: str = secrets.token_urlsafe(32)
# 60 minutes * 24 hours * 8 days = 8 days
# ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
# SERVER_NAME: str
# SERVER_HOST: AnyHttpUrl
# BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
# e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
# "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
# BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI = os.getenv('zzz')


settings = Settings()


