from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flasktask.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category='info'
# it's a gmail account
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    with app.app_context():
        db.init_app(app)
        bcrypt.init_app(app)
        login_manager.init_app(app)
        mail.init_app(app)
    # these imports must go here to prevent circular imports
    from flasktask.users.routes import users
    from flasktask.tasks.routes import tasks
    from flasktask.main.routes import main
    from flasktask.errors.error_handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(tasks)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    return app

    ##### THESE WILL BE PROVIDED IN A CONFIG FILE IN PRODUCTION
    #####

#  from flasktask import routes
