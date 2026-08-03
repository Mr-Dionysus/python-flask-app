from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, Email, EqualTo
import sqlalchemy as sa

from app import db
from app.models import User


class LoginForm(FlaskForm):
    username: StringField = StringField("Username", validators=[DataRequired()])
    password: PasswordField = PasswordField("Password", validators=[DataRequired()])
    remember_me: BooleanField = BooleanField("Remember Me")
    submit: SubmitField = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username: StringField = StringField("Username", validators=[DataRequired()])
    email: StringField = StringField("Email", validators=[DataRequired(), Email()])
    password: PasswordField = PasswordField("Password", validators=[DataRequired()])
    password2: PasswordField = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit: SubmitField = SubmitField("Register")

    def validate_username(self, username) -> None:
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email) -> None:
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError("Please use a different email.")
