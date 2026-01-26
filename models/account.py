from models import db
from datetime import datetime

class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  
    balance = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    incomes = db.relationship("Income", backref="account", lazy=True)
    expenses = db.relationship("Expense", backref="account", lazy=True)

    def __repr__(self):
        return f"<Account {self.name} | Saldo: {self.balance}>"
