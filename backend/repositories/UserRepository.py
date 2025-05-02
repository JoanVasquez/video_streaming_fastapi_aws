# 🗄️ Database imports
from db.db import get_db
from db.models.user import User


# 👥 Repository class for handling user database operations
class UserRepository:
    def add_user(self, user: User):
        with get_db() as db:
            db.add(user)
            db.commit()
            db.refresh(user)
