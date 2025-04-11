# 🗄️ Database imports
from sqlalchemy.orm import Session
from db.db import get_db
from db.models.user import User


# 👥 Repository class for handling user database operations
class UserRepository:
    # 🔧 Initialize repository with database session
    def __init__(self):
        self.db: Session = get_db()

    # ➕ Add a new user to the database
    def add_user(self, user: User):
        # Add user object to session
        self.db.add(user)
        # Commit transaction
        self.db.commit()
        # Refresh user object with generated data
        self.db.refresh(user)
