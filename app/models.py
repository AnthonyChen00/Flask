from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

#Created a class inherit from db.Model - base class for all models in Flask-SQLAlchemy
#Variables called as as db.Column() to creates information for each db entre. Can be indicated if fields should be unique and indexed (imported!)

# with database migration support, after you modify the models in your application you generate a new migration script (flask db migrate),
# you probably review it to make sure the automatic generation did the right thing,
# and then apply the changes to your development database (flask db upgrade).
# will add the migration script to source control and commit it.
# flask db downgrade will undo last migration

followers = db.Table('followers',
    db.Column('follower_id',db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author',lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin = (followers.c.followed_id == id),
        backref=db.backref('followers',lazy = 'dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        #returns an image from gravatar website services
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest,size)

    def follow(self, user):
        #appending another user to following list
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        #removing another user from following list
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self,user):
        #check through followed column to see if already following
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        #query the posts that self follows and combines with own posts ordered by timestamp
        followed =  Post.query.join(
        followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id = self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index = True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return'<Post {}>'.format(self.body)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
