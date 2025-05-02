from db.base import Base
from sqlalchemy import Column, TEXT, Integer


class User(Base):
    # 👥 User model representing the users table in the database
    __tablename__ = "users"

    # 🔑 Primary key identifier for the user
    id = Column(Integer, primary_key=True, index=True)
    # 👤 name of the user
    name = Column(TEXT, nullable=False)
    # 📧 Email address of the user (unique)
    email = Column(TEXT, unique=True, index=True, nullable=False)
    # 🔒 Cognito sub identifier for authentication (unique)
    cognito_sub = Column(TEXT, unique=True, index=True, nullable=False)
