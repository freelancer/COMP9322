from flask import request, Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from functools import wraps

import flask
import datetime
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/til.db'
app.config['AUTH_HOST'] = 'http://127.0.0.1:5000/check/'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


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


def auth_required(f):
    @wraps(f)
    def check_valid_auth_token(*args, **kwargs):
        if flask.request.headers.get('API-Token'):
            token = flask.request.headers.get('API-Token')
            check_token_response = requests.post(
                app.config['AUTH_HOST'],
                json={'token': token},
            )
            if check_token_response.status_code == 200:
                flask.request.user_id = check_token_response.json().get('user_id')
                return f(*args, **kwargs)
            else:
                return 'Invalid API token', 401
        else:
            return 'API token not supplied', 401
    return check_valid_auth_token


@app.route('/posts/', methods=['POST'])
@auth_required
def create_post():
    post_data = request.json
    post = Post(
        subject=post_data.get('subject'),
        content=post_data.get('content'),
        author_id=flask.request.user_id,
        public=bool(post_data.get('public'))
    )
    db.session.add(post)
    db.session.commit()

    tags_list = post_data.get('tags')
    if tags_list:
        for tag in tags_list:
            tag = tag.strip()
            t = Tag.query.filter_by(tag=tag).first()
            if not t:
                t = Tag(tag=tag)
                db.session.add(t)
                db.session.commit()
            pt = PostTag(post_id=post.id, tag_id=t.id)
            db.session.add(pt)
            db.session.commit()

    # TODO: DB error handling
    return jsonify({'post_id': post.id})


@app.route('/posts/', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    posts_response = []
    for post in posts:
        if post.public:
            post_tags = PostTag.query.filter_by(post_id=post.id).all()
            tags = []
            for pt in post_tags:
                tags.append(Tag.query.filter_by(id=pt.tag_id).one().tag)
            posts_response.append({
                'id': post.id,
                'subject': post.subject,
                'content': post.content,
                'author_id': post.author_id,
                'post_date': post.post_date,
                'tags': tags,
            })
    return jsonify(posts_response)


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text=str(e)), 404


if __name__ == '__main__':
    app.run(port=6000)
