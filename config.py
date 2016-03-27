import os

DEBUG = True
SECRET_KEY = "ld5rcpr6d7"
MAILGUN_KEY = "key-15f83f4a591c0a6e9f067550a967391b"

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'guestbook.db')