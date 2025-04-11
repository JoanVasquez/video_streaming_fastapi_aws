# 📦 Import required packages and modules
from fastapi import HTTPException
from repositories.UserRepository import UserRepository
import boto3
from secret_keys import SecretKeys
from helper.auth_helper import get_secret_hash
from db.models.user import User


# 🛠️ Service class for handling user operations
class UserService:
    def __init__(self):
        # 📝 Initialize repositories and configurations
        self.userRepo: UserRepository = UserRepository()
        secret_keys = SecretKeys()

        # 🔑 AWS Cognito configuration
        self.COGNITO_CLIENT_ID = secret_keys.COGNITO_CLIENT_ID
        self.COGNITO_CLIENT_SECRET = secret_keys.COGNITO_CLIENT_SECRET
        REGION_NAME = secret_keys.REGION_NAME

        # 🔌 Initialize Cognito client
        self.cognito_client = boto3.client(
            "cognito-idp", region_name=REGION_NAME
        )

    # ➕ Create a new user in Cognito and database
    def create_user(self, user):
        # 🔒 Generate secret hash for Cognito
        secret_hash = get_secret_hash(
            user.email,
            self.COGNITO_CLIENT_ID,
            self.COGNITO_CLIENT_SECRET,
        )

        # 👤 Register user in Cognito
        cognito_response = self.cognito_client.sign_up(
            ClientId=self.COGNITO_CLIENT_ID,
            Username=user.email,
            Password=user.password,
            SecretHash=secret_hash,
            UserAttributes=[
                {"Name": "email", "Value": user.email},
                {"Name": "name", "Value": user.name},
            ],
        )

        # 🔍 Extract Cognito user ID
        cognito_sub = cognito_response.get("UserSub")

        # ⚠️ Validate Cognito response
        if not cognito_sub:
            raise HTTPException(400, "Cognito did not return a valid user sub")

        # 💾 Create user in database
        new_user = User(
            name=user.name,
            email=user.email,
            cognito_sub=cognito_sub,
        )

        self.userRepo.add_user(new_user)

    # 🔐 Authenticate user and generate tokens
    def login_user(self, user):
        # 🔑 Generate secret hash for authentication
        secret_hash = get_secret_hash(
            user.email,
            self.COGNITO_CLIENT_ID,
            self.COGNITO_CLIENT_SECRET
        )

        # 🔓 Authenticate with Cognito
        cognito_response = self.cognito_client.initiate_auth(
            ClientId=self.COGNITO_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                'USERNAME': user.email,
                'PASSWORD': user.password,
                'SECRET_HASH': secret_hash
            }
        )

        # ✅ Validate authentication result
        auth_result = cognito_response.get("AuthenticationResult")

        if not auth_result:
            raise HTTPException(400, "Incorrect cognito response")

        # 🎟️ Extract authentication tokens
        access_token = auth_result.get("AccessToken")
        refresh_token = auth_result.get("RefreshToken")

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    # ✔️ Confirm user registration with OTP
    def confirm_user(self, email: str, otp: str):
        # 🔑 Generate secret hash for confirmation
        secret_hash = get_secret_hash(
            email,
            self.COGNITO_CLIENT_ID,
            self.COGNITO_CLIENT_SECRET
        )

        # 📨 Confirm signup with Cognito
        self.cognito_client.confirm_sign_up(
            ClientId=self.COGNITO_CLIENT_ID,
            Username=email,
            ConfirmationCode=otp,
            SecretHash=secret_hash
        )

    # 🔄 Refresh access token using refresh token
    def refresh_token(self, refresh_token: str, user_cognito_sub: str):
        # ⚠️ Validate required cookies
        if not refresh_token or not user_cognito_sub:
            raise HTTPException(400, "cookies cannot be null!")

        # 🔒 Generate secret hash
        secret_hash = get_secret_hash(
            user_cognito_sub,
            self.COGNITO_CLIENT_ID,
            self.COGNITO_CLIENT_SECRET
        )

        # 🔄 Request new access token from Cognito
        cognito_response = self.cognito_client.initiate_auth(
            ClientId=self.COGNITO_CLIENT_ID,
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={
                "REFRESH_TOKEN": refresh_token,
                "SECRET_HASH": secret_hash,
            },
        )

        # ✅ Validate Cognito response
        auth_result = cognito_response.get("AuthenticationResult")

        if not auth_result:
            raise HTTPException(400, "Incorrect cognito response")

        # 🎟️ Extract new access token
        access_token = auth_result.get("AccessToken")

        return access_token
