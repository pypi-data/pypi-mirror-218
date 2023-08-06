""" критические операции с пользователями """
from typing import Optional

from server.core.model import UserInfo
from server.db.config import ServerStorage
from server.db.view import UserAuthView
from common.utils.security import PasswordHash


class UserManager:
    """Класс для работы с пользователями (критические операции)"""

    def __init__(self, db: ServerStorage) -> None:
        self._db_view = UserAuthView(db)

    def add(self, user_name: str) -> Optional[UserInfo]:
        return self._db_view.add(user_name)

    def set_password(self, user_name: str, password: str) -> Optional[UserInfo]:
        pass_hash = PasswordHash.generate_password_hash(user_name, password)
        return self._db_view.password_set(user_name, pass_hash)

    def get_password_hash(self, user_name: str) -> Optional[str]:
        return self._db_view.password_get(user_name)
