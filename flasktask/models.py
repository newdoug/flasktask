from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app as app
from flasktask import db, login_manager
from flask_login import UserMixin
from flasktask.config import FieldConfig as cfg
import enum
from sqlalchemy import Integer, Enum

class PriorityEnum(enum.Enum):
    very_low = 1
    low = 2
    normal = 4
    high = 5
    severe = 7
    critical = 10

# class MyClass(Base):
#     __tablename__ = 'some_table'
#     id = Column(Integer, primary_key=True)
#     value = Column(Enum(MyEnum))
priority_files = 'priority_files'
priority_filename_map = {
    PriorityEnum.very_low: f'{priority_files}/very_low.png',
    PriorityEnum.low: f'{priority_files}/low.png',
    PriorityEnum.normal: f'{priority_files}/normal.png',
    PriorityEnum.high: f'{priority_files}/high.png',
    PriorityEnum.severe: f'{priority_files}/severe.png',
    PriorityEnum.critical: f'{priority_files}/critical.png',
}
class Task(db.Model):
    # behaves as the id
    issue_number = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(cfg.MAX_TASK_TITLE_LENGTH), nullable=False)
    created_dt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_modified_dt = db.Column(db.DateTime, nullable=True)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(cfg.MAX_TASK_STATUS_LENGTH), nullable=False, default="Open")
    priority = db.Column(Enum(PriorityEnum), nullable=True, default=PriorityEnum.normal)
    # TODO make status only a certain set of values by default, but allow creation of more *per project*
    reporter = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assignee = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    history = db.Column(db.String(100), nullable=True)
    # TODO: ??? list ???

    def __repr__(self):
        return f'Title({self.title}), description({self.description})'
    
    def getAssignee(self):
        return User.query.get(int(self.assignee))
    def getReporter(self):
        return User.query.get(int(self.reporter))
    def getPrioritySymbolFile(self, pri):
        print(f'MY PRIORITY: {pri}')
        print(f'MY PRIORITY VALUE: {pri}')
        ret = priority_filename_map.get(pri)
        ret1 = priority_filename_map.get(pri)
        print(f'RET {ret}')
        print(f'RET VALUE {ret1}')
        return ret

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(cfg.MAX_USERNAME_LENGTH), unique=True, nullable=False)
    # TODO: make this max_length shared between template and here
    email = db.Column(db.String(cfg.MAX_EMAIL_LENGTH), unique=True, nullable=False)
    # TODO store actual picture in DB
    image_file = db.Column(db.String(cfg.MAX_PROFILE_PIC_FILE_LENGTH),
            nullable=False, default=cfg.DEFAULT_PROFILE_PIC_FILENAME)
    password = db.Column(db.String(60), nullable=False)
    # TODO Shared max length for passwords - enforce in regitration form
    tasks = db.relationship('Task', foreign_keys=[Task.reporter], lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{ self.email}', {self.image_file}')"

    def get_reset_token(self, expires_sec=cfg.DEFAULT_PW_TOKEN_EXPIRATION_SEC):
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

