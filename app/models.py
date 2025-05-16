from typing import Optional
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    surname: Mapped[Optional[str]]
    name: Mapped[Optional[str]]
    email: Mapped[Optional[str]] = mapped_column(unique=True)
    hashed_password: Mapped[Optional[str]]
