from typing import Optional
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    surname: Mapped[Optional[str]]
    name: Mapped[Optional[str]]
    email: Mapped[Optional[str]] = mapped_column(unique=True)
    hashed_password: Mapped[Optional[str]]

    def __repr__(self):
        return f'<User> {self.id} {self.name} {self.email}'

    def set_password(self, password: str):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str):
        return self.hashed_password is not None and \
            check_password_hash(self.hashed_password, password)


@login_manager.user_loader
def load_user(user_id: int):
    return db.session.query(User).get(user_id)
