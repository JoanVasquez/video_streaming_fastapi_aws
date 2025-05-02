# 🔐 Authentication router module
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
# 📋 Import request models
from pydantic_models.auth_models import (
    SignRequest,
    LoginRequest,
    ConfirmSignupRequest,
)
# 🔒 Import auth middleware
from db.middleware.auth_middleware import get_current_user
# 👥 Import user service
from services.UserService import UserService

# 🛠️ Router setup
router = APIRouter()


# 📝 User signup endpoint
# ➡️ Creates a new user account
@router.post("/signup")
def signup_user(
    data: SignRequest,
    user_service: UserService = Depends(UserService),
):
    try:
        # 👤 Create new user
        user_service.create_user(data)

        # ✅ Return success message
        return {
            "message": (
                "Signup successful. Please verify your email if required"
            )
        }
    except Exception as e:
        # ❌ Handle errors
        raise HTTPException(400, f"Cognito signup exception {e}")


# 🔑 Login endpoint
# ➡️ Authenticates user and returns tokens
@router.post("/login")
def login_user(
    data: LoginRequest,
    response: Response,
    user_service: UserService = Depends(UserService),
):
    try:

        # 🎫 Get auth tokens
        access_token, refresh_token = user_service.login_user(data).values()

        # 🍪 Set access token cookie
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
        )

        # 🔄 Set refresh token cookie
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
        )

        # ✅ Return success message
        return {
            "message": "User logged in successfully"
        }
    except Exception as e:
        # ❌ Handle errors
        raise HTTPException(400, f"Cognito signin exception {e}")


# ✔️ Signup confirmation endpoint
# ➡️ Verifies user email with OTP
@router.post("/confirm-signup")
def confirm_signup(
    data: ConfirmSignupRequest,
    user_service: UserService = Depends(UserService),
):
    try:

        # 📨 Confirm user email
        user_service.confirm_user(data.email, data.otp)

        # ✅ Return success message
        return {
            "message": "User confirmed successfully!"
        }
    except Exception as e:
        # ❌ Handle errors
        raise HTTPException(400, f"Cognito confirmation exception {e}")


# 🔄 Token refresh endpoint
# ➡️ Issues new access token using refresh token
@router.post("/refresh")
def refresh_token(
    refresh_token: str = Cookie(None),
    user_cognito_sub: str = Cookie(None),
    response: Response = None,
):
    try:

        # 🎫 Get new access token
        access_token = UserService().refresh_token(
            refresh_token, user_cognito_sub
        )

        # 🍪 Set new access token cookie
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
        )

        # ✨ Return success message
        return {"message": "Access token refreshed!"}
    except Exception as e:
        # ❌ Handle errors
        raise HTTPException(400, f"Cognito refresh exception: {e}")


# 👤 Protected user info endpoint
# ➡️ Returns authenticated user details
@router.get("/me")
def protected_route(user=Depends(get_current_user)):
    # ✅ Return authenticated user info
    return {"message": "You are authenticated!", "user": user}
