from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask import (render_template, url_for, flash,
                           redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flasktask import db
from flasktask.models import Task
from flasktask.tasks.forms import TaskForm


tasks = Blueprint('tasks', __name__)

@tasks.route('/task/new/', methods=['GET', 'POST'])
@login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        assignee = form.assignee.data.id if form.assignee.data else None
        task = Task(title=form.title.data, description=form.description.data,
                reporter=current_user.id, assignee=assignee)
        db.session.add(task)
        db.session.commit()
        flash(f'The task #{task.issue_number} was successfully created!', 'success')
        # TODO: redirect to detail view of new task.
        return redirect(url_for('main.home'))
    return render_template('create_task.html', title='New Task', form=form,
            legend='Create New Task')

@tasks.route('/task/<int:task_id>')
@login_required
def task_details(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('task_details.html', title='Task Details', task=task)

@tasks.route('/task/update/<int:task_id>/', methods=['GET', 'POST'])
@login_required
def task_update(task_id):
    # FIXME: the button says "create"
    task = Task.query.get_or_404(task_id)
    if task.reporter != current_user.id and task.assignee != current_user.id:
        abort(403)
    form = TaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.assignee = form.assignee.data
        db.session.commit()
        flash('This post has been updated', 'success')
        return redirect(url_for('tasks.task_details', task_id=task.issue_number))
    elif request.method == 'GET':
        form.title.data = task.title
        form.description.data = task.description
        form.assignee.data = task.assignee
    return render_template('create_task.html', title='Update Task', task=task,
            legend='Update Task', form=form)

@tasks.route('/task/delete/<int:task_id>/', methods=['POST'])
@login_required
def task_delete(task_id):
    task = Task.query.get_or_404(task_id)
    if task.assignee != current_user.id and task.reporter != current_user.id:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Task has been deleted.', 'success')
    return redirect(url_for('main.home'))

