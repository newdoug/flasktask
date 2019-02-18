from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app as app
from flasktask import db, login_manager
from flask_login import UserMixin


class Task(db.Model):
    # behaves as the id
    issue_number = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    created_dt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_modified_dt = db.Column(db.DateTime, nullable=True)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Open")
    #  priority = db.Column(db.String(20), nullable=False, default="Normal")
    # TODO make status and priority only a certain set of values
    reporter = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assignee = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    history = db.Column(db.String(100), nullable=True)
    # TODO: ??? list ???

    def __repr__(self):
        return 'Title(' + self.title + '), description(' + self.description + ')'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    # TODO: make this max_length shared between template and here
    email = db.Column(db.String(120), unique=True, nullable=False)
    # TODO store actual picture in DB
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # TODO Shared max length for passwords - enforce in regitration form
    tasks = db.relationship('Task', foreign_keys=[Task.reporter], lazy=True)

    def __repr__(self):
        return "User('" + self.username + "', '" + self.email + "', " + self.image_file + "')"

    def get_reset_token(self, expires_sec=1000):
        ser = Serializer(app.config['SECRET_KEY'], expires_sec)
        return ser.dumps({'user_id': self.id}).decode('utf-8')
    @staticmethod
    def verify_reset_token(token):
        ser = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = ser.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
