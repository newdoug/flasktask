import os
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask import current_app as app
from flasktask import db, bcrypt, mail
from flasktask.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flasktask.models import User, Task
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash(f'You are already logged in as {current_user}!', 'success')
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,
                password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        # TODO fstring when python >3.6
        flash(f'Account created for username \'{form.username.data}\'!', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f'You are already logged in as \'{current_user}\'!', 'success')
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Successfully logged in with email \'{form.email.data}\'!', 'success')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password \
                    combination.', 'danger')
            return render_template('login.html', title='Login', form=form)
    return render_template('login.html', title='Login', form=form)

@users.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You were successfully logged out. Thank you for visiting!', 'success')
    return redirect(url_for('users.login'))


def save_picture(form_picture_data):
    random_hex = os.urandom(16) 
    filename, extension = os.path.splitext(form_picture_data.filename)
    picture_filename = str(random_hex) + extension
    picture_path = os.path.join(app.root_path, 'static/images/profile_pictures/',
            picture_filename)
    form_picture_data.save(picture_path)
    return picture_filename

@users.route('/account/', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/profile_pictures/' + current_user.image_file)
    return render_template('account.html', title='Account',
            image_file=image_file, form=form)


@users.route('/user/assigned/')
def user_assigned_tasks():
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=current_user.username).first_or_404()
    per_page = 3
    tasks = Task.query.filter_by(assignee=user.id)\
            .order_by(Task.created_dt.desc())\
            .paginate(page=page, per_page=per_page)
    return render_template('user_assigned_tasks.html', tasks=tasks, user=user)


def send_reset_password_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
            sender='noreply@noreply.com',
            recipients=[user.email])
    msg.body = 'To reset your password, visit the following link: \n ' + \
            url_for('users.reset_token', token=token, _external=True) + \
            ' \nIf you did not make this request then simply ignore this email and no changes will be made.'
    mail.send(msg)


@users.route("/reset_password/", methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm()
    if current_user.is_authenticated:
        if request.method == 'GET':
            form.email.data = current_user.email
            return render_template('reset_request.html', title='Reset Password', form=form)
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_password_email(user)
        flash(f'An email has been sent to \'{form.email.data}\' with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


