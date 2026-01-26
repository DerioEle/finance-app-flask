from flask import Blueprint, render_template, request, redirect, url_for
from models.expense import Expense
from models.account import Account
from models import db
from datetime import datetime

expenses_bp = Blueprint("expenses", __name__, url_prefix="/expenses")


@expenses_bp.route("/")
def list_expenses():
    expenses = Expense.query.all()
    return render_template("expenses/expenses.html", expenses=expenses)


@expenses_bp.route("/new", methods=["GET", "POST"])
def create_expense():
    accounts = Account.query.all()

    if request.method == "POST":
        expense = Expense(
            description=request.form["description"],
            amount=float(request.form["amount"]),
            category=request.form["category"],
            payment_method=request.form["payment_method"],
            date=datetime.strptime(request.form["date"], "%Y-%m-%d").date(),
            account_id=int(request.form["account_id"])
        )

        account = Account.query.get(expense.account_id)
        account.balance -= expense.amount

        db.session.add(expense)
        db.session.commit()

        return redirect(url_for("expenses.list_expenses"))

    return render_template("expenses/new.html", accounts=accounts)


@expenses_bp.route("/<int:id>")
def detail_expense(id):
    expense = Expense.query.get_or_404(id)
    return render_template("expenses/detail.html", expense=expense)


@expenses_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_expense(id):
    expense = Expense.query.get_or_404(id)
    accounts = Account.query.all()

    if request.method == "POST":
        old_amount = expense.amount
        old_account = expense.account

        expense.description = request.form["description"]
        expense.amount = float(request.form["amount"])
        expense.category = request.form["category"]
        expense.payment_method = request.form["payment_method"]
        expense.date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
        expense.account_id = int(request.form["account_id"])

        old_account.balance += old_amount
        new_account = Account.query.get(expense.account_id)
        new_account.balance -= expense.amount

        db.session.commit()
        return redirect(url_for("expenses.list_expenses"))

    return render_template(
        "expenses/edit.html",
        expense=expense,
        accounts=accounts
    )


@expenses_bp.route("/delete/<int:id>", methods=["POST"])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    account = expense.account

    account.balance += expense.amount
    db.session.delete(expense)
    db.session.commit()

    return redirect(url_for("expenses.list_expenses"))
