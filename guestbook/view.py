import json
import hashlib
from functools import wraps
from flask import render_template, redirect, url_for, request, session
from guestbook import app, db
from .models import *
from .message import message

def ifLogin(fun):
    @wraps(fun)
    def check():
        if 'isactive' in session and session['isactive']:
            return fun()
        return redirect(url_for('index'))
    return check

def ifNotLogin(fun):
    @wraps(fun)
    def check():
        if 'isactive' in session and session['isactive']:
            return redirect(url_for('index'))
        return fun()
    return check

def showIndexPage():
    if 'isactive' in session and session['isactive']:
        usermail = session['usermail']
        userId = session['userId']
        user = User.query.get(userId)
        urls = [
            {"url": _.pageurl, "id": _.id} 
            for _ in Commentboard.query.filter_by(user=user)
        ]
        return render_template('index.html', user=usermail, urls=urls)
    
    return render_template('index.html')

@ifNotLogin
def registerUser():
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
def loginUser():
    usermail = request.form['usermail']
    password = request.form['password']
    
    if usermail and password:
        password = md5hash(password)
        user = User.query.filter_by(usermail=usermail).first()
        if user and user.password == password:
            session['usermail'] = user.usermail
            session['isactive'] = user.isactive
            session['userId'] = user.id
            print(session['usermail'], session['isactive'])
        else:
            return message["fail_to_login"]
    else:
        return message["field_cantbe_empty"]

    return message["successful"]

@ifLogin
def logoutUser():
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
    pageUrl = request.form['pageUrl']
    userId = session['userId']
    user = User.query.get(userId)

    if not Commentboard.query.filter_by(pageurl=pageUrl).first():
        board = Commentboard(pageUrl, user)
        db.session.add(board)
        db.session.commit()
    else:
        return 'this page url is regist'

    return redirect(url_for('index'))

def delMyBoard():
    pageid = request.args['board_id']
    page = Commentboard.query.get(pageid)
    db.session.delete(page)
    db.session.commit()
    return 'del'

def getBoardComment(board_id):
    comments = []
    pageid = board_id
    board = Commentboard.query.get(pageid)
    for com in board.comments:
        comments.append(com.mesg)

    return json.dumps(comments)

def addNewComment(board_id):
    pageid = board_id
    mesg = request.form['mesg']
    board = Commentboard.query.get(pageid)
    comment = Comments(mesg, board)
    db.session.add(comment)
    db.session.commit()

    return getBoardComment(board_id)


def leaveComment(board_id):
    if request.method == 'GET':
        return getBoardComment(board_id)
    if request.method == 'POST':
        return addNewComment(board_id)
    else:
        return 'fail'

def showBoard():
    return 'showboard'

def md5hash(password):
    m = hashlib.md5()
    m.update(password.encode('utf-8'))
    return m.hexdigest()
