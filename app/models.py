from app import db

#Created a class inherit from db.Model - base class for all models in Flask-SQLAlchemy
#Variables called as as db.Column() to creates information for each db entre. Can be indicated if fields should be unique and indexed (imported!)
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)
