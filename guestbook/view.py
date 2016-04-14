from functools import wraps
from flask import render_template, redirect, url_for, request, session, jsonify
from guestbook import app, db

from .models import *
from .helper import *
from .message import success, fail
from .sendmail import Verificationletter


def ifLogin(f):
    @wraps(f)
    def check():
        if 'userId' in session:
            return f()
        return redirect(url_for('index'))
    return check


def ifNotLogin(f):
    @wraps(f)
    def check():
        if 'userId' in session:
            return redirect(url_for('index'))
        return f()
    return check


def checkFormIsEmpty(f):
    @wraps(f)
    def check():
        for key in request.form:
            if request.form[key] == '':
                return jsonify(fail["field_cantbe_empty"])
        return f()
    return check


def showIndexPage():
    if 'userId' in session:
        usermail = session['usermail']
        return render_template('index.html', user=usermail)

    return render_template('index.html')


@ifNotLogin
@checkFormIsEmpty
def userRegister():
    usermail = request.form['usermail'].strip()
    nickname = request.form['nickname'].strip()
    passwd1 = request.form['password1'].strip()
    passwd2 = request.form['password2'].strip()

    if not (passwd1 == passwd2):
        return jsonify(fail["passwd_confirm"])

    if not checkMailValid(usermail):
        return jsonify(fail['email_invalid'])

    if not checkPasswdValid(passwd1):
        return jsonify(fail['password_invalid'])

    if User.query.filter_by(usermail=usermail).first() is not None:
        return jsonify(fail["user_is_exist"])

    if User.query.filter_by(nickname=nickname).first() is not None:
        return jsonify(fail["user_is_exist"])
    else:
        password = md5hash(passwd1)
        user = User(usermail, nickname, password)
        db.session.add(user)
        sendToken(user)
        return jsonify(success(message='we’ll send you an email'))


@ifNotLogin
@checkFormIsEmpty
def userLogin():
    usermail = request.form['usermail'].strip()
    password = request.form['password'].strip()

    password = md5hash(password)
    user = User.query.filter_by(usermail=usermail).first()

    if user is None:
        return jsonify(fail["fail_to_login"])

    if not (user.password == password):
        return jsonify(fail["fail_to_login"])

    if not user.isactive:
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
        urls.append({"id": com.id, "pageurl": com.pageurl})

    return jsonify(success(data=urls))


@ifLogin
@checkFormIsEmpty
def addMyBoard():
    page_url = request.form['board_url']
    userId = session['userId']
    user = User.query.get(userId)

    if Commentboard.query.filter_by(pageurl=page_url).first() is not None:
        return jsonify(fail['page_is_exist'])
    else:
        board = Commentboard(page_url, user)
        db.session.add(board)
        return jsonify(success())


@ifLogin
def delMyBoard():
    board_id = request.args['board_id']
    page = Commentboard.query.get(board_id)

    if page is None:
        return jsonify(fail['page_is_not_exist'])
    else:
        db.session.delete(page)
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

@checkFormIsEmpty
def addcomment():
    text = request.form['text']
    pageid = request.form['board_id']
    board = Commentboard.query.get(pageid)
    user = User.query.get(session['userId'])

    if board is None:
        return jsonify(fail['page_is_not_exist'])
    else:
        comment = Comment(text, board, user)
        db.session.add(comment)
        return jsonify(success())
