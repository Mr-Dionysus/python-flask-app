from flask import render_template
from app import app


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "MrDionysus"}
    posts = [
        {"author": {"username": "Linus"}, "body": "Linux is the best"},
        {"author": {"username": "Oleg"}, "body": "Test"},
    ]
    return render_template("index.html", title="Home", user=user, posts=posts)


@app.route("/test")
def test():
    return "test 23123123"
