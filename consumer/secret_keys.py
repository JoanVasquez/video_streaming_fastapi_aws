# 🔧 Import required libraries for configuration management
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# 📥 Load environment variables from .env file
load_dotenv()


# 🔐 Class to store and validate secret configuration keys
class SecretKeys(BaseSettings):
    # 🌎 AWS region name
    REGION_NAME: str
    # 📨 SQS queue URL for video processing
    AWS_SQS_VIDEO_PROCESSING: str
    # 🚀 ECS cluster ARN for container orchestration
    AWS_ECS_CLUSTER_ARN: str
    # 📋 ECS task definition ARN for container configuration
    AWS_ECS_CLUSTER_TASK_ARN: str
    # 🌐 Public subnet A for VPC networking
    AWS_VPC_PUBLIC_SUBNET_A: str
    # 🌐 Public subnet B for VPC networking
    AWS_VPC_PUBLIC_SUBNET_B: str
    # 🔒 Private subnet A for VPC networking
    AWS_VPC_PRIVATE_SUBNET_A: str
    # 🔒 Private subnet B for VPC networking
    AWS_VPC_PRIVATE_SUBNET_B: str
    # 🛡️ Security group for VPC access control
    AWS_VPC_SECURITY_GROUP: str
