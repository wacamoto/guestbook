from guestbook import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usermail = db.Column(db.String(64), index=True, unique=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), index=True)
    isactive = db.Column(db.Boolean)

    def __init__(self, usermail, nickname, password):
        self.usermail = usermail
        self.nickname = nickname
        self.password = password
        self.isactive = False

    def __repr__(self):
        return '<User %s>' % self.usermail


class Commentboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pageurl = db.Column(db.String(64), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='commentboard')
    # comment = db.relationship('Comment', backref='commentboard',
    #                         cascade='all, delete-orphan')

    def __init__(self, url, user):
        self.pageurl = url
        self.user = user

    def __repr__(self):
        return '<page %s>' % self.pageurl


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(64), index=True)
    board_id = db.Column(db.Integer, db.ForeignKey('commentboard.id'))
    commentboard = db.relationship('Commentboard', backref='comment')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='comment')

    def __init__(self, text, board, user):
        self.text = text
        self.commentboard = board
        self.user = user

    def __repr__(self):
        return '<comment to %s>' % self.commentboard


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='token')

    def __init__(self, token, user):
        self.token = token
        self.user = user

    def __repr__(self):
        return '<token %s>' % self.user
