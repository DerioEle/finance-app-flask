# 💰 Finance App – Flask

Aplicação web de **controle financeiro pessoal**, desenvolvida com **Python + Flask**, que permite gerenciar **contas, receitas e despesas**, com dashboard e visualização detalhada dos dados.

O projeto foi desenvolvido com foco em:
- Código organizado
- UX simples e profissional
- Separação clara entre backend e frontend
- Facilidade de evolução

---

## 🚀 Funcionalidades

- Dashboard com:
  - Saldo total
  - Total de receitas
  - Total de despesas
  - Filtro por mês e ano
  - Gráfico de evolução mensal
- CRUD completo de:
  - Contas
  - Receitas
  - Despesas
- Tela de detalhes (somente leitura)
- Edição e exclusão com **modal de confirmação**
- Layout responsivo básico
- Interface em HTML/CSS puro (sem frameworks)

---

## 🧱 Tecnologias Utilizadas

- Python 3.x
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML5
- CSS3
- JavaScript (básico)

---

## 📂 Estrutura do Projeto

```
finance_app/
│
├── app.py
├── routes/
│   ├── accounts.py
│   ├── incomes.py
│   └── expenses.py
│
├── models/
│   ├── account.py
│   ├── income.py
│   └── expense.py
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── accounts/
│   ├── incomes/
│   ├── expenses/
│   └── partials/
│       └── delete_modal.html
│
├── static/
│   └── css/
│       └── style.css
│
├── instance/
│   └── database.db   (gerado automaticamente)
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Como Rodar o Projeto Localmente

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/SEU_USUARIO/finance-app-flask.git
cd finance-app-flask
```

---

### 2️⃣ Criar e ativar o ambiente virtual

```bash
python -m venv venv
```

**Windows**
```bash
venv\Scripts\activate
```

**Linux / Mac**
```bash
source venv/bin/activate
```

---

### 3️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

---

## 🗄️ Como Criar o Banco de Dados (SQLite)

Abra o terminal **na raiz do projeto** e execute:

```bash
python
```

No interpretador Python:

```python
from app import app
from models import db

with app.app_context():
    db.create_all()
```

Para sair:

```python
exit()
```

---

## ▶️ Executar a Aplicação

```bash
flask run
```

Ou:

```bash
python app.py
```

Acesse:

```
http://127.0.0.1:5000
```

---

## 👤 Autor

Desenvolvido por **Dério Crisóstomo**
