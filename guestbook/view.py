import re
import time
import hashlib
from functools import wraps
from flask import render_template, redirect, url_for, request, session, jsonify
from guestbook import app, db
from .models import *
from .message import success, fail
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
        return render_template('index.html', user=usermail)

    return render_template('index.html')

@ifNotLogin
def userRegister():
    usermail = request.form['usermail'].strip()
    nickname = request.form['nickname'].strip()
    passwd1 = request.form['password1'].strip()
    passwd2 = request.form['password2'].strip()
    
    if usermail == '' and nickname == '' and passwd1 == '' and passwd2 == '':
        return jsonify(fail["field_cantbe_empty"])
    
    if not (passwd1 == passwd2):
        return jsonify(fail["passwd_confirm"])

    if checkMailValid(usermail) == False:
        return jsonify(fail['email_invalid'])

    if checkPasswdValid(passwd1) == False:
        return jsonify(fail['password_invalid'])

    if User.query.filter_by(usermail=usermail).first() is not None:
        return jsonify(fail["user_is_exist"])

    if User.query.filter_by(nickname=nickname).first() is not None:
        return jsonify(fail["user_is_exist"])
    else:
        password = md5hash(passwd1)
        user = User(usermail, nickname, password)
        db.session.add(user)
        db.session.commit()
        sendToken(user)
        return jsonify(success(message='we’ll send you an email'))

@ifNotLogin
def userLogin():
    usermail = request.form['usermail'].strip()
    password = request.form['password'].strip()
    
    if usermail == '' and password == '':
        return jsonify(fail["field_cantbe_empty"])

    password = md5hash(password)
    user = User.query.filter_by(usermail=usermail).first()
    
    if user is None:
        return jsonify(fail["fail_to_login"])

    if not (user.password == password):
        return jsonify(fail["fail_to_login"])

    if user.isactive == False:
        return jsonify(fail['user_unactive'])
    else:
        session['usermail'] = user.usermail
        session['userId'] = user.id
        return jsonify(success())

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

    return jsonify(success(data=urls))

@ifLogin
def addMyBoard():
    page_url = request.form['board_url']
    userId = session['userId']
    user = User.query.get(userId)

    if Commentboard.query.filter_by(pageurl=page_url).first() is not None:
        return jsonify(fail['page_is_exist'])
    else:
        board = Commentboard(page_url, user)
        db.session.add(board)
        db.session.commit()
        return jsonify(success())

@ifLogin
def delMyBoard():
    board_id = request.args['board_id']
    page = Commentboard.query.get(board_id)

    if page is None:
        return jsonify(fail['page_is_not_exist'])
    else:
        db.session.delete(page)
        db.session.commit()
        return jsonify(success())

def verifyUser():
    key = request.args['key']
    token = Token.query.filter_by(token=key).first()

    if token is None:
        return jsonify(fail['fail_to_verify'])
    else:
        user = token.user
        user.isactive = True
        db.session.add(user)
        db.session.delete(token)
        db.session.commit()
        session['usermail'] = user.usermail
        session['userId'] = user.id

        return redirect(url_for('index'))

def showBoard():
    board_id = request.args['board_id']
    return render_template('comment.html', id=board_id)

def getcomment():
    comments = []
    pageid = request.args['board_id']
    board = Commentboard.query.get(pageid)
    
    if pageid == '':
        return jsonify(fail['field_cantbe_empty'])

    if board is None:
        return jsonify(fail['page_is_not_exist'])
    else:
        for com in board.comment:
            comments.append({
                "text": com.text,
                "user": com.user.nickname
            })

        return jsonify(success(data=comments))

def addcomment():
    text = request.form['text']
    pageid = request.form['board_id']
    board = Commentboard.query.get(pageid)
    user = User.query.get(session['userId'])
    
    if pageid == '' and text == '':
        return jsonify(fail['field_cantbe_empty'])

    if board is None:
        return jsonify(fail['page_is_not_exist'])
    else:
        comment = Comment(text, board, user)
        db.session.add(comment)
        db.session.commit()
        return jsonify(success())

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

def tokenGenerator(usermail):
    m = hashlib.md5()
    token = usermail + str(time.time()) + app.config['SECRET_KEY']
    m.update(token.encode('utf-8'))
    return m.hexdigest()

def sendToken(user):
    token = tokenGenerator(user.usermail)
    acesstoken = Token(token, user)
    Verificationletter(user.usermail, token)
    print('usermail=>{0}\nkey=>{1}'.format(user.usermail, token))

    db.session.add(acesstoken)
    db.session.commit()
