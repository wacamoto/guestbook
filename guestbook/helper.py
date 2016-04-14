import re
import time
import hashlib
import config

from guestbook import db
from .models import Token
from .sendmail import Verificationletter


def checkMailValid(email):
    regex = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(regex, email)


def checkPasswdValid(passwd):
    return any(_.isdigit() for _ in passwd) and \
           any(_.isalpha() for _ in passwd) and \
           len(passwd) > 10


def md5hash(password):
    m = hashlib.md5()
    password += config.SECRET_KEY
    m.update(password.encode('utf-8'))
    return m.hexdigest()


def tokenGenerator(usermail):
    m = hashlib.md5()
    token = usermail + str(time.time()) + config.SECRET_KEY
    m.update(token.encode('utf-8'))
    return m.hexdigest()


def sendToken(user):
    token = tokenGenerator(user.usermail)
    acesstoken = Token(token, user)
    # Verificationletter(user.usermail, token)
    print('usermail=>{0}\nkey=>{1}'.format(user.usermail, token))

    db.session.add(acesstoken)
    db.session.commit()
