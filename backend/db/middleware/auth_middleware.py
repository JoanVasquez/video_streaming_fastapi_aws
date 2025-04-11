# 🔐 Authentication and User Management Module
from fastapi import Cookie, HTTPException
import boto3
from secret_keys import SecretKeys

# ☁️ Initialize Cognito client
cognito_client = boto3.client(
    "cognito-idp",
    region_name=SecretKeys().REGION_NAME,
)


# 👤 Helper function to fetch user details from Cognito
def _get_user_from_cognito(access_token: str):
    try:
        # Call Cognito API to get user info
        user_res = cognito_client.get_user(AccessToken=access_token)

        # 📝 Extract user attributes into dictionary
        return {
            attr["Name"]: attr["Value"]
            for attr in user_res.get("UserAttributes", [])
        }
    except Exception:
        # ❌ Handle errors when fetching user
        raise HTTPException(500, "Error fetching user")


# 🔑 Main function to get current authenticated user
def get_current_user(access_token: str = Cookie(None)):
    # Check if user is logged in
    if not access_token:
        raise HTTPException(401, "User not logged in!")
    print(access_token)
    return _get_user_from_cognito(access_token)
