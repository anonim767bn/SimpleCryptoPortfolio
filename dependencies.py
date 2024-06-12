from db import get_user_from_db
from models import User
from security import verify_password

def get_current_user(username: str, password: str, session_factory) -> User|bool:
    user = get_user_from_db(session_factory, username)
    if not user or not verify_password(password, user.hash_password):
        return False
    return user

    