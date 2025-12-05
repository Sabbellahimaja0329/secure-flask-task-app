from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .forms import RegisterForm, LoginForm
from . import models
import bcrypt

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data.strip()
        email = form.email.data.strip().lower()
        password = form.password.data.encode('utf-8')
        # check existing
        if models.get_user_by_email(email):
            flash('Email already registered', 'warning')
            return render_template('register.html', form=form)
        pw_hash = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
        models.create_user(name, email, pw_hash, role='user')
        flash('Registered. Please login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        password = form.password.data.encode('utf-8')
        user = models.get_user_by_email(email)
        if user and bcrypt.checkpw(password, user['password_hash'].encode('utf-8')):
            session.clear()
            session['user_id'] = user['id']
            session['role'] = user['role']
            session['user_name'] = user['name']
            flash('Logged in', 'success')
            return redirect(url_for('tasks.dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out', 'info')
    return redirect(url_for('auth.login'))