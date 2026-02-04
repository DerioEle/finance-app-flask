"""
Decoradores customizados para autenticação e autorização
"""
from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user


def login_required_custom(f):
    """
    Decorator customizado para exigir login e exibir mensagem amigável
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Você precisa fazer login para acessar esta página.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function
