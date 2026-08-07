from datetime import datetime, timezone
from hashlib import md5
from typing import override

import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

from app import db, login


class User(db.Model, UserMixin):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[str | None] = so.mapped_column(sa.String(256))
    about_me: so.Mapped[str | None] = so.mapped_column(sa.String(300))
    last_seen: so.Mapped[datetime | None] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    posts: so.WriteOnlyMapped["Post"] = so.relationship(back_populates="author")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def avatar(self, size) -> str:
        digest: str = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"

    @login.user_loader
    def load_user(id) -> User | None:
        return db.session.get(User, int(id))

    @override
    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(300))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc)
    )
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    author: so.Mapped[User] = so.relationship(back_populates="posts")

    @override
    def __repr__(self) -> str:
        return f"<Post {self.body}>"
