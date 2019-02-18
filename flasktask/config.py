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
    RECAPTCHA_PUBLIC_KEY = '6LfCE5IUAAAAALYkPVGVTLKBlzEgzB4JsK3349Ii'
    RECAPTCHA_PRIVATE_KEY = ''
    RECAPTCHA_OPTIONS = {'theme': 'black'}
