from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.account import Account
from models import db

accounts_bp = Blueprint("accounts", __name__, url_prefix="/accounts")

@accounts_bp.route("/")
@login_required
def list_accounts():
    accounts = Account.query.all()
    return render_template("accounts/accounts.html", accounts=accounts)

@accounts_bp.route("/new", methods=["GET", "POST"])
@login_required
def create_account():
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            type_ = request.form.get("type", "").strip()
            balance_str = request.form.get("balance", "0")
            
            # Validações
            if not name:
                flash("Nome da conta é obrigatório", "error")
                return render_template("accounts/new.html")
            
            if not type_:
                flash("Tipo de conta é obrigatório", "error")
                return render_template("accounts/new.html")
            
            try:
                balance = float(balance_str)
            except ValueError:
                flash("Saldo deve ser um número válido", "error")
                return render_template("accounts/new.html")
            
            if balance < 0:
                flash("Saldo não pode ser negativo", "error")
                return render_template("accounts/new.html")

            account = Account(name=name, type=type_, balance=balance)
            db.session.add(account)
            db.session.commit()
            
            flash(f"Conta '{name}' criada com sucesso!", "success")
            return redirect(url_for("accounts.list_accounts"))
        
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao criar conta: {str(e)}", "error")
            return render_template("accounts/new.html")

    return render_template("accounts/new.html")
