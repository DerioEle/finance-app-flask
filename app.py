from flask import Flask, render_template
from flask_login import LoginManager, login_required, current_user
from models import db
from models.user import User
from models.expense import Expense
from models.income import Income

app = Flask(__name__)

app.config["SECRET_KEY"] = "dev-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


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
    # Totais
    total_income = (
        db.session.query(db.func.coalesce(db.func.sum(Income.amount), 0))
        .scalar()
    )

    total_expense = (
        db.session.query(db.func.coalesce(db.func.sum(Expense.amount), 0))
        .scalar()
    )

    total_balance = total_income - total_expense

    # Dados para gráficos (temporariamente vazios)
    labels = []
    income_values = []
    expense_values = []

    return render_template(
        "dashboard.html",
        total_income=total_income,
        total_expense=total_expense,
        total_balance=total_balance,
        labels=labels,
        income_values=income_values,
        expense_values=expense_values
    )


if __name__ == "__main__":
    app.run(debug=True)
