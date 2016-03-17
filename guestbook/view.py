import re
import time
import json
import random
import hashlib
from functools import wraps
from flask import render_template, redirect, url_for, request, session
from guestbook import app, db
from .models import *
from .message import message
from .sendmail import Verificationletter


def ifLogin(fun):
    @wraps(fun)
    def check():
        if 'userId' in session:
            return fun()
        return redirect(url_for('index'))
    return check

def ifNotLogin(fun):
    @wraps(fun)
    def check():
        if 'userId' in session:
            return redirect(url_for('index'))
        return fun()
    return check

def showIndexPage():
    if 'userId' in session:
        usermail = session['usermail']
        userId = session['userId']
        return render_template('index.html', user=usermail)
    
    return render_template('index.html')

@ifNotLogin
def userRegister():
    usermail = request.form['usermail'].strip()
    nickname = request.form['nickname'].strip()
    passwd1 = request.form['password1'].strip()
    passwd2 = request.form['password2'].strip()
    
    if not (usermail and nickname and passwd1 and passwd2):
        return message["field_cantbe_empty"]
    
    if not (passwd1 == passwd2):
        return message["passwd_confirm"]

    if not checkMailValid(usermail):
        return message['email_unvalid']

    if not checkPasswdValid(passwd1):
        return message['password_unvalid']

    if User.query.filter_by(usermail=usermail).first():
        return message["user_is_exist"]

    if User.query.filter_by(nickname=nickname).first():
        return message["user_is_exist"]
    else:
        password = md5hash(passwd1)
        user = User(usermail, nickname, password)
        db.session.add(user)
        db.session.commit()
        return message["successful"]

@ifNotLogin
def userLogin():
    usermail = request.form['usermail'].strip()
    password = request.form['password'].strip()
    
    if not (usermail and password):
        return message["field_cantbe_empty"]

    password = md5hash(password)
    user = User.query.filter_by(usermail=usermail).first()
    
    if not (user and user.password == password):
        return message["fail_to_login"]

    if not user.isactive:
        return message['user_unactive']
    else:
        session['usermail'] = user.usermail
        session['userId'] = user.id
        return message["successful"]

@ifLogin
def userLogout():
    session.clear()
    return redirect(url_for('index'))

@ifLogin
def getMyBoard():
    urls = []
    userId = session['userId']
    user = User.query.get(userId)
    for com in user.commentboard:
        urls.append({"id": com.id, "pageurl":com.pageurl})

    return json.dumps(urls)

@ifLogin
def addNewBoard():
    page_url = request.form['page_url']
    userId = session['userId']
    user = User.query.get(userId)

    if Commentboard.query.filter_by(pageurl=page_url).first():
        return message['page_is_exist']
    else:
        board = Commentboard(page_url, user)
        db.session.add(board)
        db.session.commit()
        return message['successful']

@ifLogin
def delMyBoard():
    page_id = request.args['board_id']
    page = Commentboard.query.get(page_id)
    
    if not page:
        return message['page_is_not_exist']
    else:
        db.session.delete(page)
        db.session.commit()
        return message['successful']

def verifyUser():
    key = request.args['key']
    token = Token.query.filter_by(token=key)

    if token:
        user = token.user
        user.isactive = True
        db.session.delete(token)
        db.session.commit()
    else:
        return 'fail to Verify'

    return message['successful']

def showBoard():
    page_id = request.args['page_id']
    return render_template('comment.html', id=page_id)

def getcomment():
    comments = []
    pageid = request.args['board_id']
    board = Commentboard.query.get(pageid)
    
    if not pageid:
        return message['field_cantbe_empty']

    if not board:
        return message['page_is_not_exist']
    else:
        for com in board.comments:
            comments.append(com.mesg)

        return json.dumps(comments)

def addcomment():
    mesg = request.form['mesg']
    pageid = request.form['board_id']
    board = Commentboard.query.get(pageid)
    
    if not (pageid and mesg):
        return message['field_cantbe_empty']

    if not board:
        return message['page_is_not_exist']
    else:
        comment = Comments(mesg, board)
        db.session.add(comment)
        db.session.commit()
        return message['successful']

def checkMailValid(email):
    regex = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(regex, email)

def checkPasswdValid(passwd):
    return any(c.isdigit() for c in passwd) and \
           any(c.isalpha() for c in passwd) 

def md5hash(password):
    m = hashlib.md5()
    password += app.config['SECRET_KEY']
    m.update(password.encode('utf-8'))
    return m.hexdigest()

def gentoken(usermail):
    m = hashlib.md5()
    token = usermail + str(time.time()) + app.config['SECRET_KEY']
    m.update(token.encode('utf-8'))
    return m.hexdigest()

def sendtoken(userId):
    user = User.query.get(userId)
    token = gentoken(user.usermail)
    acesstoekn = Token(token, user)
    Verificationletter(acesstoekn)

    db.session.add(acesstoekn)
    db.session.commit()
