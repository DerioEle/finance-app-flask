from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from models.user import User
from models import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()

        if user and user.check_password(request.form["password"]):
            login_user(user)
            return redirect(url_for("dashboard"))

        flash("Email ou senha inválidos", "error")

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        # Verifica se email já existe
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Este email já está cadastrado. Faça login.", "error")
            return redirect(url_for("auth.login"))

        user = User(name=name, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for("dashboard"))

    return render_template("auth/register.html")



@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
