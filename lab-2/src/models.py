import datetime
from db import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(800), nullable=False)
    author_id = db.Column(db.Integer)
    public = db.Column(db.Boolean, default=False)
    post_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(10), unique=True)
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class PostTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(Post.id))
    tag_id = db.Column(db.Integer, db.ForeignKey(Tag.id))

