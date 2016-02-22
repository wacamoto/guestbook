from guestbook import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usermail = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), index =True)
    comments = db.relationship('Commentboard', backref='user')

    def __init__(self, usermail, password):
        self.usermail = usermail
        self.password = password
        self.is_authenticated= True
        self.is_active = True
        self.is_anonymous = True

    def __repr__(self):
        return '<User %s>' % self.usermail

    def get_id(self):
        return self.id


class Commentboard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(64), index=True, unique=True)
    comments = db.relationship('Comments', backref='comment')
    UserID = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return '<page %s>' % self.url

    
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64), index=True)
    mesg = db.Column(db.String(64), index=True)
    commentID = db.Column(db.Integer, db.ForeignKey('commentboard.id'))

    def __init__(self, user, mesg):
        self.user = user
        self.mesg = mesg

    def __repr__(self):
        return '<comments from %s>' % self.user
