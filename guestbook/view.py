import hashlib
from flask import render_template, redirect, url_for, request
from flask.ext.login import login_user, logout_user, current_user

from guestbook import app, db, loginManager
from .models import User, Commentboard, Comments


@loginManager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        usermail = request.form['usermail']
        password = request.form['password']
        password = md5hash(password)
        user = User(usermail, password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        usermail = request.form['usermail']
        password = request.form['password']
        password = md5hash(password)
        user = User.query.filter_by(usermail=usermail).first()
        if user and user.password == password:
            return redirect(url_for('index'))
        else:
            return 'fail to login'

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/newboard', methods=['POST'])
def newComment():
    return 'new a comment'

@app.route('/delboard', methods=['POST'])
def delComment():
    return 'del a comment'

@app.route('/comments/<id>', methods=['GET', 'POST'])
def leaveComment():
    if request.method == 'POST':
        return 'comments [GET]'
    else:
        return 'add a comment'

def md5hash(password):
    m = hashlib.md5()
    m.update(password.encode('utf-8'))
    return m.hexdigest()