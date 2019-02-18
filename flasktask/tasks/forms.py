from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from flasktask.models import User


def _get_all_users():
    return User.query.with_entities(User.id, User.username).all()
class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    # TODO: make this searchable. Also place small image next to each username
    assignee = QuerySelectField('Assignee',
            query_factory=_get_all_users,
            allow_blank=True,
            get_pk=lambda a: a.id,
            get_label='username',
            blank_text='No assignee')
    submit = SubmitField('Create')
