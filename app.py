from flask import Flask, render_template, request
from flask_login import LoginManager, login_required, current_user
from models import db
from models.user import User
from models.expense import Expense
from models.income import Income
from config import Config
from datetime import datetime, timedelta
from sqlalchemy import extract

app = Flask(__name__)

# Carrega configurações do arquivo config.py
app.config.from_object(Config)

db.init_app(app)


login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except Exception:
        return None


from routes.auth import auth_bp
from routes.expenses import expenses_bp
from routes.incomes import incomes_bp
from routes.accounts import accounts_bp

app.register_blueprint(auth_bp)
app.register_blueprint(expenses_bp)
app.register_blueprint(incomes_bp)
app.register_blueprint(accounts_bp)


@app.route("/")
@login_required
def dashboard():
    # Pega filtros da requisição
    selected_year = request.args.get("year", type=int)
    selected_month = request.args.get("month", type=int)
    show_pie = request.args.get("show_pie", type=int)
    
    # Totais gerais com filtros
    total_income_query = db.session.query(db.func.coalesce(db.func.sum(Income.amount), 0))
    total_expense_query = db.session.query(db.func.coalesce(db.func.sum(Expense.amount), 0))
    
    # Aplica filtros se existirem
    if selected_year:
        total_income_query = total_income_query.filter(extract('year', Income.date) == selected_year)
        total_expense_query = total_expense_query.filter(extract('year', Expense.date) == selected_year)
    
    if selected_month:
        total_income_query = total_income_query.filter(extract('month', Income.date) == selected_month)
        total_expense_query = total_expense_query.filter(extract('month', Expense.date) == selected_month)
    
    total_income = total_income_query.scalar()
    total_expense = total_expense_query.scalar()
    total_balance = total_income - total_expense

    # Dados para gráfico de linha (por mês)
    labels = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    income_values = [0] * 12
    expense_values = [0] * 12
    
    # Query para receitas por mês
    year_filter = selected_year or datetime.now().year
    
    incomes_by_month = db.session.query(
        extract('month', Income.date).label('month'),
        db.func.sum(Income.amount).label('total')
    ).filter(
        extract('year', Income.date) == year_filter
    )
    
    expenses_by_month = db.session.query(
        extract('month', Expense.date).label('month'),
        db.func.sum(Expense.amount).label('total')
    ).filter(
        extract('year', Expense.date) == year_filter
    )
    
    # Se houver filtro de mês, mostrar apenas aquele mês
    if selected_month:
        incomes_by_month = incomes_by_month.filter(extract('month', Income.date) == selected_month)
        expenses_by_month = expenses_by_month.filter(extract('month', Expense.date) == selected_month)
    
    incomes_by_month = incomes_by_month.group_by(extract('month', Income.date)).all()
    expenses_by_month = expenses_by_month.group_by(extract('month', Expense.date)).all()
    
    # Popula os valores
    for month_data in incomes_by_month:
        if month_data.month:
            income_values[int(month_data.month) - 1] = float(month_data.total or 0)
    
    for month_data in expenses_by_month:
        if month_data.month:
            expense_values[int(month_data.month) - 1] = float(month_data.total or 0)
    
    # Dados para gráfico de pizza (por categoria) com filtros
    category_labels = []
    category_values = []
    
    if show_pie:
        expenses_by_category = db.session.query(
            Expense.category,
            db.func.sum(Expense.amount).label('total')
        )
        
        # Aplica filtros ao gráfico de pizza também
        if selected_year:
            expenses_by_category = expenses_by_category.filter(extract('year', Expense.date) == selected_year)
        
        if selected_month:
            expenses_by_category = expenses_by_category.filter(extract('month', Expense.date) == selected_month)
        
        expenses_by_category = expenses_by_category.group_by(Expense.category).all()
        
        for category_data in expenses_by_category:
            if category_data.category:
                category_labels.append(category_data.category)
                category_values.append(float(category_data.total or 0))

    return render_template(
        "dashboard.html",
        total_income=total_income,
        total_expense=total_expense,
        total_balance=total_balance,
        labels=labels,
        income_values=income_values,
        expense_values=expense_values,
        selected_year=selected_year,
        selected_month=selected_month,
        show_pie=show_pie,
        category_labels=category_labels,
        category_values=category_values
    )




if __name__ == "__main__":
    app.run(debug=True)
