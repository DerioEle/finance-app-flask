from flask import Flask
from flask_migrate import Migrate
from config import Config
from models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    # IMPORTA blueprints
    from routes.dashboard import dashboard_bp
    from routes.accounts import accounts_bp
    from routes.incomes import incomes_bp
    from routes.expenses import expenses_bp

    # REGISTRA blueprints (UMA VEZ SÓ)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(accounts_bp)
    app.register_blueprint(incomes_bp)
    app.register_blueprint(expenses_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
