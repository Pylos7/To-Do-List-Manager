from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from flask_migrate import Migrate
import secrets
from datetime import datetime
from models import User, Task, DueDate, Priority


app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_hex(16)  # Set a secret key for session encryption
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///list_manager_database.db'  # Set the database URI
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

# Create the User loader function
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    form = TaskForm()
    if form.validate_on_submit():
        task_name = form.task_name.data
        priority = form.priority.data
        status = form.status.data
        notes = form.notes.data
        created_at = datetime.now()
        
        new_task = Task(task_name=task_name, priority=priority, status=status, notes=notes, created_at=created_at, user=current_user)
        db.session.add(new_task)
        db.session.commit()
        
        return redirect(url_for('home'))
    
    tasks = Task.query.filter_by(user=current_user).all()
    return render_template('home.html', tasks=tasks, form=form)


@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    
    if form.validate_on_submit():
        task.task_name = form.task_name.data
        task.priority = form.priority.data
        task.status = form.status.data
        task.notes = form.notes.data
        task.updated_at = datetime.now()
        
        db.session.commit()
        
        return redirect(url_for('home'))
    
    return render_template('update_task.html', form=form)


@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    if task.user != current_user:
        abort(403)  # User is not authorized to delete the task
    
    db.session.delete(task)
    db.session.commit()
    
    return redirect(url_for('home'))

login_manager.init_app(app)

# Create the Task Form
class TaskForm(FlaskForm):
    task_name = StringField('Task Name', validators=[DataRequired()])
    priority = StringField('Priority', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()])
    notes = StringField('Notes')
    submit = SubmitField('Add Task')


if __name__ == '__main__':
    app.run(debug=True)


