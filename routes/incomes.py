from flask import Blueprint, render_template, request, redirect, url_for
from models.income import Income
from models.account import Account
from models import db
from datetime import datetime

incomes_bp = Blueprint("incomes", __name__, url_prefix="/incomes")


@incomes_bp.route("/")
def list_incomes():
    incomes = Income.query.all()
    return render_template("incomes/incomes.html", incomes=incomes)


@incomes_bp.route("/new", methods=["GET", "POST"])
def create_income():
    accounts = Account.query.all()

    if request.method == "POST":
        income = Income(
            description=request.form["description"],
            amount=float(request.form["amount"]),
            category=request.form["category"],
            date=datetime.strptime(request.form["date"], "%Y-%m-%d").date(),
            account_id=int(request.form["account_id"])
        )

        account = Account.query.get(income.account_id)
        account.balance += income.amount

        db.session.add(income)
        db.session.commit()

        return redirect(url_for("incomes.list_incomes"))

    return render_template("incomes/new.html", accounts=accounts)


@incomes_bp.route("/<int:id>")
def detail_income(id):
    income = Income.query.get_or_404(id)
    return render_template("incomes/detail.html", income=income)


@incomes_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_income(id):
    income = Income.query.get_or_404(id)
    accounts = Account.query.all()

    if request.method == "POST":
        old_amount = income.amount
        old_account = income.account

        income.description = request.form["description"]
        income.amount = float(request.form["amount"])
        income.category = request.form["category"]
        income.date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
        income.account_id = int(request.form["account_id"])

        old_account.balance -= old_amount
        new_account = Account.query.get(income.account_id)
        new_account.balance += income.amount

        db.session.commit()
        return redirect(url_for("incomes.list_incomes"))

    return render_template(
        "incomes/edit.html",
        income=income,
        accounts=accounts
    )


@incomes_bp.route("/delete/<int:id>", methods=["POST"])
def delete_income(id):
    income = Income.query.get_or_404(id)
    account = income.account

    account.balance -= income.amount
    db.session.delete(income)
    db.session.commit()

    return redirect(url_for("incomes.list_incomes"))
