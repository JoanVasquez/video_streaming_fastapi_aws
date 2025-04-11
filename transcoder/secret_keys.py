# 🔐 Configuration for managing secret keys and environment variables
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class SecretKeys(BaseSettings):
    # 🔑 AWS authentication credentials
    REGION_NAME: str = ""  # Secret name for AWS Secrets Manager
    AWS_ACCESS_KEY_ID: str = ""  # AWS access key ID
    AWS_SECRET_ACCESS_KEY: str = ""  # AWS secret access key

    # 📦 S3 bucket configuration
    S3_BUCKET: str = ""  # Main S3 bucket name
    S3_KEY: str = ""  # S3 key/path
    S3_PROCESSED_VIDEOS_BUCKET: str = ""  # Bucket for processed videos

    # 🌐 API configuration
    BACKEND_URL: str = ""  # Backend service URL
