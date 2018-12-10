import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #information for email server goes here
        # to use local host as server:
        #   1.) run this on a seperate terminal
        #       python3 -m smtpd -n -c DebuggingServer localhost:8025
        #   2.) run these commands in venv
        #       MAIL_SERVER=localhost
        #       MAIL_PORT=8025
        #       FLASK_DEBUG=0
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['tomokoNALS@gmail.com']

    #pagination
    POSTS_PER_PAGE = 20
