from pydantic import BaseModel


# 📝 Request model for user signup
class SignRequest(BaseModel):
    name: str      # User's full name
    email: str     # User's email address
    password: str  # User's password


# 🔑 Request model for user login
class LoginRequest(BaseModel):
    email: str     # User's email address
    password: str  # User's password


# ✅ Request model for confirming user signup
class ConfirmSignupRequest(BaseModel):
    email: str     # User's email address
    otp: str       # One-time password for verification
