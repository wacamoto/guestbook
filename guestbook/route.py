import hashlib

from functools import wraps
from flask import render_template, redirect, url_for, request, session
from guestbook import app, db

from .models import User, Commentboard
from .view import showRegisterPage, registerUser, showLoginPage, loginUser


def loginCheckDecorator(fun):
    @wraps(fun)
    def check():
        if 'isactive' in session and session['isactive']:
            usermail = session['usermail']
            userId = session['userId']
            user = User.query.get(userId)
            urls = [_.pageurl for _ in Commentboard.query.filter_by(user=user)]
            return render_template('index.html', user=usermail, urls=urls)
        return fun()
    return check

@app.route('/', methods=['GET'])
@loginCheckDecorator
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
@loginCheckDecorator
def register():
    if request.method == 'GET':
        return showRegisterPage()
    else:
        return registerUser()

@app.route('/login', methods=['GET', 'POST'])
@loginCheckDecorator
def login():
    if request.method == 'GET':
        return showLoginPage()
    else:
        return loginUser()

@app.route('/logout')
def logout():
    if 'usermail' in session:
        session['isactive'] = False
        session.pop('usermail', None)

    return redirect(url_for('index'))

@app.route('/newboard', methods=['POST'])
def newComment():
    pageUrl = request.form['pageUrl']
    userId = session['userId']
    user = User.query.get(userId)
    board = Commentboard(pageUrl, user)
    db.session.add(board)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delboard', methods=['POST'])
def delComment():
    return 'del a comment'

@app.route('/comments/<int:boardId>', methods=['GET', 'POST'])
def leaveComment():
    cb = Commentboard.query.get(boardID)
    if request.method == 'GET':
        comments = cb.comments.all()
        return str(comments)
    else:
        msg = request.form['comment']
        com = Comments(msg, cb)
        db.session.add(com)
        db.session.commmit()
        return ''
