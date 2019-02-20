import os

class Config:
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    SECRET_KEY = 'SOME CSRF TOKEN'
    # TODO: switch to better DB like postgres
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    # recaptcha is v2 "I am not a robot" button
    RECAPTCHA_USE_SSL = True
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
    RECAPTCHA_OPTIONS = {'theme': 'black'}

class FieldConfig:
    # users
    MIN_USERNAME_LENGTH = 2
    MAX_USERNAME_LENGTH = 50
    # only have email max length due to DB requiring one
    # so, will conveniently add to form validations as well
    MAX_EMAIL_LENGTH = 120
    MAX_PROFILE_PIC_FILE_LENGTH = 30
    DEFAULT_PROFILE_PIC_FILENAME = 'default.jpg'

    # tasks
    MAX_TASK_TITLE_LENGTH = 100
    MAX_TASK_STATUS_LENGTH = 20

    # unencrypted/hashed/salted lengths
    MIN_PW_LENGTH = 6
    MAX_PW_LENGTH = 30

    DEFAULT_PW_TOKEN_EXPIRATION_SEC = 3600

