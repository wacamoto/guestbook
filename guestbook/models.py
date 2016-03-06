from guestbook import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usermail = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), index =True)
    isactive = db.Column(db.Boolean)
    
    def __init__(self, usermail, password):
        self.usermail = usermail
        self.password = password
        self.isactive = True

    def __repr__(self):
        return '<User %s>' % self.usermail

    def get_id(self):
        return self.id


class Commentboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pageurl = db.Column(db.String(64), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='commentboard')
    
    def __init__(self, url, user):
        self.pageurl = url
        self.user = user

    def __repr__(self):
        return '<page %s>' % self.pageurl


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mesg = db.Column(db.String(64), index=True)
    board_id = db.Column(db.Integer, db.ForeignKey('commentboard.id'))
    commentboard = db.relationship('Commentboard', backref='comments')

    def __init__(self, mesg, board):
        self.mesg = mesg
        self.commentboard = board

    def __repr__(self):
        return '<comments to %s>' % self.commentboard
