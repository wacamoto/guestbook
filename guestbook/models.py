from guestbook import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usermail = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), index =True)
    isactive = db.Column(db.Boolean)
    Commentboard = db.relationship('Commentboard')

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
    user = db.relationship('User')
    # comment = db.relationship('Comments', backref='comment')
    
    def __init__(self, url, user):
        self.pageurl = url
        self.user = user

    def __repr__(self):
        return '<page %s>' % self.url

    
# class Comments(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     mesg = db.Column(db.String(64), index=True)
#     boardID = db.Column(db.Integer, db.ForeignKey('commentboard.id'))

#     def __init__(self, mesg, board):
#         self.mesg = mesg
#         self.commentboard = board

#     def __repr__(self):
#         return '<comments from %s>' % self.user
