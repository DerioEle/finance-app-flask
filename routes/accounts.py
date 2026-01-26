from flask import Blueprint, render_template, request, redirect, url_for
from models.account import Account
from models import db

accounts_bp = Blueprint("accounts", __name__, url_prefix="/accounts")

@accounts_bp.route("/")
def list_accounts():
    accounts = Account.query.all()
    return render_template("accounts/accounts.html", accounts=accounts)

@accounts_bp.route("/new", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        name = request.form["name"]
        type_ = request.form["type"]
        balance = float(request.form["balance"])

        account = Account(name=name, type=type_, balance=balance)
        db.session.add(account)
        db.session.commit()

        return redirect(url_for("accounts.list_accounts"))

    return render_template("accounts/new.html")
