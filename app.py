from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from flask_migrate import Migrate

from models import User, Task, DueDate, Priority


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Set a secret key for session encryption
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Set the database URI
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

if __name__ == '__main__':
    app.run(debug=True)
