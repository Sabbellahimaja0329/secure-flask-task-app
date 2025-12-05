from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DateField
from wtforms.validators import InputRequired, Email, Length

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=100)])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=255)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8)])

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired(), Length(max=255)])
    description = TextAreaField('Description', validators=[Length(max=2000)])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[InputRequired()])
    status = SelectField('Status', choices=[('todo','To do'),('in_progress','In progress'),('done','Done')])

class CSRFOnlyForm(FlaskForm):
    """Empty form only to provide CSRF token for simple actions (delete button)."""
    pass