from flask import Blueprint, render_template, request
from models.account import Account
from models.income import Income
from models.expense import Expense
from models import db
from sqlalchemy import extract

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def index():
    # 🔹 Filtros
    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)
    show_pie = request.args.get("show_pie") == "1"

    # 🔹 Saldo total (não filtrado)
    accounts = Account.query.all()
    total_balance = sum(a.balance for a in accounts)

    income_query = Income.query
    expense_query = Expense.query

    if year:
        income_query = income_query.filter(extract("year", Income.date) == year)
        expense_query = expense_query.filter(extract("year", Expense.date) == year)

    if month:
        income_query = income_query.filter(extract("month", Income.date) == month)
        expense_query = expense_query.filter(extract("month", Expense.date) == month)

    total_income = income_query.with_entities(db.func.sum(Income.amount)).scalar() or 0
    total_expense = expense_query.with_entities(db.func.sum(Expense.amount)).scalar() or 0

    # 🔹 Evolução mensal (linha)
    monthly_incomes = (
        Income.query
        .filter(extract("year", Income.date) == (year or extract("year", Income.date)))
        .with_entities(
            extract("month", Income.date),
            db.func.sum(Income.amount)
        )
        .group_by(extract("month", Income.date))
        .order_by(extract("month", Income.date))
        .all()
    )

    monthly_expenses = (
        Expense.query
        .filter(extract("year", Expense.date) == (year or extract("year", Expense.date)))
        .with_entities(
            extract("month", Expense.date),
            db.func.sum(Expense.amount)
        )
        .group_by(extract("month", Expense.date))
        .order_by(extract("month", Expense.date))
        .all()
    )

    income_dict = {int(m): float(v) for m, v in monthly_incomes}
    expense_dict = {int(m): float(v) for m, v in monthly_expenses}

    months = list(range(1, 13))
    income_values = [income_dict.get(m, 0) for m in months]
    expense_values = [expense_dict.get(m, 0) for m in months]

    # 🔹 Pizza (opcional)
    category_labels = []
    category_values = []

    if show_pie:
        expenses_by_category = (
            expense_query
            .with_entities(
                Expense.category,
                db.func.sum(Expense.amount)
            )
            .group_by(Expense.category)
            .all()
        )

        category_labels = [c for c, _ in expenses_by_category]
        category_values = [float(v) for _, v in expenses_by_category]

    return render_template(
        "dashboard.html",
        total_balance=total_balance,
        total_income=total_income,
        total_expense=total_expense,
        income_values=income_values,
        expense_values=expense_values,
        category_labels=category_labels,
        category_values=category_values,
        selected_year=year,
        selected_month=month,
        show_pie=show_pie
    )
