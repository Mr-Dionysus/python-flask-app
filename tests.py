import os

os.environ["DATABASE_URL"] = "sqlite://"

import unittest
from datetime import UTC, datetime, timedelta
from typing import override

from app import app, db
from app.models import Post, User


class UserModelCase(unittest.TestCase):
    @override
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    @override
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username="test", email="test@example.com")
        u.set_password("password")
        self.assertFalse(u.check_password("wrong"))
        self.assertTrue(u.check_password("password"))

    def test_avatar(self):
        u = User(username="john", email="john@example.com")
        self.assertEqual(
            u.avatar(128),
            (
                "https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=identicon&s=128"
            ),
        )

    def test_follow(self):
        u1 = User(username="test1", email="test1@example.com")
        u2 = User(username="test2", email="test2@example.com")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        following = db.session.scalars(u1.following.select()).all()
        followers = db.session.scalars(u2.followers.select()).all()
        self.assertEqual(following, [])
        self.assertEqual(followers, [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.following_count(), 1)
        self.assertEqual(u2.followers_count(), 1)
        u1_following = db.session.scalars(u1.following.select()).all()
        u2_followers = db.session.scalars(u2.followers.select()).all()
        self.assertEqual(u1_following[0].username, "test2")
        self.assertEqual(u2_followers[0].username, "test1")

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.following_count(), 0)
        self.assertEqual(u2.followers_count(), 0)

    def test_follow_posts(self):
        u1 = User(username="test1", email="test1@example.com")
        u2 = User(username="test2", email="test2@example.com")
        u3 = User(username="test3", email="test3@example.com")
        u4 = User(username="test4", email="test4@example.com")
        db.session.add_all([u1, u2, u3, u4])

        now = datetime.now(UTC)
        p1 = Post(
            body="post from test1", author=u1, timestamp=now + timedelta(seconds=1)
        )
        p2 = Post(
            body="post from test2", author=u2, timestamp=now + timedelta(seconds=4)
        )
        p3 = Post(
            body="post from test3", author=u3, timestamp=now + timedelta(seconds=3)
        )
        p4 = Post(
            body="post from test4", author=u4, timestamp=now + timedelta(seconds=2)
        )
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        u1.follow(u2)
        u1.follow(u4)
        u2.follow(u3)
        u3.follow(u4)
        db.session.commit()

        f1 = db.session.scalars(u1.following_posts()).all()
        f2 = db.session.scalars(u2.following_posts()).all()
        f3 = db.session.scalars(u3.following_posts()).all()
        f4 = db.session.scalars(u4.following_posts()).all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


if __name__ == "__main__":
    unittest.main(verbosity=2)
