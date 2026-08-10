import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
    ValidationError,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length

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


class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    about_me = TextAreaField("About me", validators=[Length(min=0, max=300)])
    submit = SubmitField("Submit")

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(
                sa.select(User).where(User.username == self.original_username)
            )
            if user is not None:
                raise ValidationError("Please use a different username")
