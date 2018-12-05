from app import db
from datetime import datetime

#Created a class inherit from db.Model - base class for all models in Flask-SQLAlchemy
#Variables called as as db.Column() to creates information for each db entre. Can be indicated if fields should be unique and indexed (imported!)

# with database migration support, after you modify the models in your application you generate a new migration script (flask db migrate),
# you probably review it to make sure the automatic generation did the right thing,
# and then apply the changes to your development database (flask db upgrade).
# will add the migration script to source control and commit it.
# flask db downgrade will undo last migration
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author',lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index = True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return'<Post {}>'.format(self.body)
