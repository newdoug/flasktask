
from flask import render_template, request, Blueprint
from flasktask.models import Task
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    # TODO: only display tasks either assigned to us or we've reported
    per_page = 3
    page = request.args.get('page', 1, type=int)
    tasks = Task.query.order_by(Task.created_dt.desc()).paginate(page=page,
            per_page=per_page)
    return render_template('home.html', tasks=tasks, user=current_user)

@main.route('/about')
def about():
    return render_template('about.html', title='About')
