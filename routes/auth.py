from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from models.user import User
from models import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Se usuário já está logado, redireciona para dashboard
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        
        # Validação básica
        if not email or not password:
            flash("Email e senha são obrigatórios", "error")
            return render_template("auth/login.html")
        
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user, remember=request.form.get("remember", False))
            flash(f"Bem-vindo, {user.name}!", "success")
            return redirect(url_for("dashboard"))

        flash("Email ou senha inválidos", "error")

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # Se usuário já está logado, redireciona para dashboard
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        password_confirm = request.form.get("password_confirm", "")

        # Validações
        if not all([name, email, password, password_confirm]):
            flash("Todos os campos são obrigatórios", "error")
            return render_template("auth/register.html")
        
        if len(password) < 6:
            flash("A senha deve ter pelo menos 6 caracteres", "error")
            return render_template("auth/register.html")
        
        if password != password_confirm:
            flash("As senhas não coincidem", "error")
            return render_template("auth/register.html")
        
        if len(name) < 3:
            flash("O nome deve ter pelo menos 3 caracteres", "error")
            return render_template("auth/register.html")

        # Verifica se email já existe
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Este email já está cadastrado. Faça login.", "error")
            return redirect(url_for("auth.login"))

        user = User(name=name, email=email)
        user.set_password(password)

        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash(f"Bem-vindo, {user.name}! Sua conta foi criada com sucesso.", "success")
            return redirect(url_for("dashboard"))
        except Exception as e:
            db.session.rollback()
            flash("Erro ao criar conta. Tente novamente.", "error")
            return render_template("auth/register.html")

    return render_template("auth/register.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("Você foi desconectado com sucesso.", "success")
    return redirect(url_for("auth.login"))

    flash("Você foi desconectado com sucesso.", "success")
    return redirect(url_for("auth.login"))
