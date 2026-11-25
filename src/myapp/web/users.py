from flask import Blueprint, render_template, request, redirect,url_for

from myapp.extensions import db
from myapp.models import User

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.get("/")
def index():
    users = db.session.scalars(db.select(User)).all()
    return render_template("users/index.html", users=users)

@users_bp.post("/",strict_slashes=False)
def create():
    name = request.form.get("name")
    email = request.form.get("email")

    user = User(name=name, email = email)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("users.index"))
