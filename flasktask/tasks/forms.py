from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from flasktask.models import User, PriorityEnum

priority_choices = [
    (PriorityEnum.normal.value, "Normal"),
    (PriorityEnum.very_low.value, "Very Low"),
    (PriorityEnum.low.value, "Low"),
    (PriorityEnum.high.value, "High"),
    (PriorityEnum.severe.value, "Severe"),
    (PriorityEnum.critical.value, "Critical"),
]


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
                                blank_text='No assignee'
                                )
    priority = SelectField('Priority',
                           choices=priority_choices,
                           coerce=int
                           )
    submit = SubmitField('Create')
