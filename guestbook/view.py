import hashlib
from flask import render_template, redirect, url_for, request, session
from guestbook import app, db
from .models import User, Commentboard

def showRegisterPage():
    return render_template('register.html')

def showLoginPage():
    return render_template('login.html')

def registerUser():
    usermail = request.form['usermail']
    password = request.form['password']
    password = md5hash(password)
    user = User(usermail, password)
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('login'))

def loginUser():
    usermail = request.form['usermail']
    password = request.form['password']
    password = md5hash(password)
    user = User.query.filter_by(usermail=usermail).first()
    if user and user.password == password:
        session['usermail'] = str(user.usermail)
        session['isactive'] = user.isactive
        session['userId'] = user.id
        return redirect(url_for('index'))
    else:
        return 'fail to login'

def md5hash(password):
    m = hashlib.md5()
    m.update(password.encode('utf-8'))
    return m.hexdigest()