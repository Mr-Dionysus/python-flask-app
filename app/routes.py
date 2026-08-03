from urllib.parse import urlsplit
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
import sqlalchemy as sa


@app.route("/")
@app.route("/index")
@login_required
def index():
    posts = [
        {"author": {"username": "Linus"}, "body": "Linux is the best"},
        {"author": {"username": "Oleg"}, "body": "Test"},
    ]
    return render_template("index.html", title="Home", posts=posts)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration completed!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        query_find_user = sa.select(User).where(User.username == form.username.data)
        user = db.session.scalar(query_find_user)
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username of password")
            return redirect(url_for("login"))
        _ = login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    _ = logout_user()
    return redirect(url_for("index"))
