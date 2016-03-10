import time
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
        user = User.query.get(userId)
        return render_template('index.html', user=usermail)
    
    return render_template('index.html')

@ifNotLogin
def userRegister():
    usermail = request.form['usermail']
    passwd1 = request.form['password1']
    passwd2 = request.form['password2']
    
    if usermail and passwd1 and passwd2:
        if passwd1 == passwd2:
            if not User.query.filter_by(usermail=usermail).first():
                password = md5hash(passwd1)
                user = User(usermail, password)
                db.session.add(user)
                db.session.commit()
            else:
                return message["user_is_exist"]
        else:
            return message["passwd_confirm"]
    else:
        return message["field_cantbe_empty"]

    return message["successful"]

@ifNotLogin
def userLogin():
    usermail = request.form['usermail']
    password = request.form['password']
    
    if usermail and password:
        password = md5hash(password)
        user = User.query.filter_by(usermail=usermail).first()
        if user and user.password == password:
            if user.isactive:
                session['usermail'] = user.usermail
                session['userId'] = user.id
            else:
                return message['user_unactive']
        else:
            return message["fail_to_login"]
    else:
        return message["field_cantbe_empty"]

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
    page_id = request.args['page_id']
    userId = session['userId']
    user = User.query.get(userId)

    if not Commentboard.query.get(page_id):
        board = Commentboard(page_id, user)
        db.session.add(board)
        db.session.commit()
    else:
        return message['page_is_exist']

    return message['successful']

@ifLogin
def delMyBoard():
    page_id = request.args['board_id']
    page = Commentboard.query.get(page_id)
    
    if page:
        db.session.delete(page)
        db.session.commit()
    else:
        return message['page_is_not_exist']
    
    return message['successful']

def showBoard():
    return 'showboard'

def verifyUser():
    key = request.form['key']
    token = Token.query.filter_by(token = key)

    if token:
        user = token.user
        user.isactive = True
        db.session.delete(token)
        db.session.commit()
    else:
        return 'fail to Verify'

    return message['successful']

def getcomment():
    comments = []
    pageid = request.args['board_id']
    board = Commentboard.query.get(pageid)
    
    if pageid:
        if board:
            for com in board.comments:
                comments.append(com.mesg)
        else:
            return message['page_is_not_exist']
    else:
        return message['field_cantbe_empty']
    
    return json.dumps(comments)

def addcomment():
    mesg = request.form['mesg']
    pageid = request.args['board_id']
    board = Commentboard.query.get(pageid)
    if pageid and mesg:
        if board:
            comment = Comments(mesg, board)
            db.session.add(comment)
            db.session.commit()
        else:
            return message['page_is_not_exist']
    else:
        return message['field_cantbe_empty']
    
    return getBoardComment(board_id)

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
