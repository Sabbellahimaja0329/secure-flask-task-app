from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from .forms import TaskForm, CSRFOnlyForm
from . import models
from functools import wraps

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please login', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapped

def admin_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('Admin access required', 'danger')
            return redirect(url_for('tasks.dashboard'))
        return f(*args, **kwargs)
    return wrapped

@tasks_bp.route('/dashboard')
@login_required
def dashboard():
    cnx = models.get_db()
    cur = cnx.cursor(dictionary=True)
    if session.get('role') == 'admin':
        cur.execute("SELECT t.*, u.name as owner FROM tasks t JOIN users u ON t.created_by = u.id ORDER BY t.created_at DESC")
    else:
        cur.execute("SELECT t.*, u.name as owner FROM tasks t JOIN users u ON t.created_by = u.id WHERE created_by = %s ORDER BY t.created_at DESC", (session['user_id'],))
    tasks = cur.fetchall()
    cur.close(); cnx.close()

    csrf_form = CSRFOnlyForm()     # <<< create form instance
    return render_template('dashboard.html', tasks=tasks, csrf_form=csrf_form)

@tasks_bp.route('/create', methods=['GET','POST'])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        cnx = models.get_db()
        cur = cnx.cursor()
        cur.execute("INSERT INTO tasks (title, description, due_date, status, created_by) VALUES (%s,%s,%s,%s,%s)",
                    (form.title.data.strip(), form.description.data.strip(), form.due_date.data, form.status.data, session['user_id']))
        cur.close(); cnx.close()
        flash('Task created', 'success')
        return redirect(url_for('tasks.dashboard'))
    return render_template('task_form.html', form=form, action="Create")

@tasks_bp.route('/edit/<int:task_id>', methods=['GET','POST'])
@login_required
def edit_task(task_id):
    cnx = models.get_db()
    cur = cnx.cursor(dictionary=True)
    cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cur.fetchone()
    if not task:
        flash('Task not found', 'warning'); cur.close(); cnx.close(); return redirect(url_for('tasks.dashboard'))
    if session.get('role') != 'admin' and task['created_by'] != session['user_id']:
        flash('Not authorized to edit', 'danger'); cur.close(); cnx.close(); return redirect(url_for('tasks.dashboard'))

    form = TaskForm(data=task)
    if form.validate_on_submit():
        cur.execute("UPDATE tasks SET title=%s, description=%s, due_date=%s, status=%s WHERE id=%s",
                    (form.title.data.strip(), form.description.data.strip(), form.due_date.data, form.status.data, task_id))
        cur.close(); cnx.close()
        flash('Task updated', 'success')
        return redirect(url_for('tasks.dashboard'))
    cur.close(); cnx.close()
    return render_template('task_form.html', form=form, action="Edit")

@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    cnx = models.get_db()
    cur = cnx.cursor(dictionary=True)
    cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cur.fetchone()
    if not task:
        flash('Task not found', 'warning'); cur.close(); cnx.close(); return redirect(url_for('tasks.dashboard'))
    if session.get('role') != 'admin' and task['created_by'] != session['user_id']:
        flash('Not authorized to delete', 'danger'); cur.close(); cnx.close(); return redirect(url_for('tasks.dashboard'))
    # delete safely
    cur = cnx.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    cur.close(); cnx.close()
    flash('Task deleted', 'info')
    return redirect(url_for('tasks.dashboard'))