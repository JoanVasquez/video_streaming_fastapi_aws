from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # Load data 📂


# INFO: Set .env variables 🔒
class SecretKeys(BaseSettings):
    COGNITO_CLIENT_ID: str = ""
    COGNITO_CLIENT_SECRET: str = ""
    REGION_NAME: str = ""
    POSTGRES_DB_USER: str = ""
    POSTGRES_DB_PASSWORD: str = ""
    POSTGRES_DB_NAME: str = ""
    POSTGRES_DB_PORT: str = ""
