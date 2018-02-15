from flask import request, Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from functools import wraps
from flasgger import Swagger

import flask
import requests

from models import Post, PostTag, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/til.db'
app.config['AUTH_HOST'] = 'http://127.0.0.1:5000/check/'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['SWAGGER'] = {
    'title': 'Today I Learned',
    'Description': 'The API for Today I Learned',
    'uiversion': 2
}
swagger = Swagger(app)


def auth_required(f):
    @wraps(f)
    def check_valid_auth_token(*args, **kwargs):
        if flask.request.headers.get('TIL-API-TOKEN'):
            token = flask.request.headers.get('TIL-API-TOKEN')
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
    """ Create a new post
    ---
    parameters:
      - in: "body"
        name: "body"
        description: "Create a new post"
        required: true
        schema:
          $ref: "#/definitions/CreatePostRequest"
    responses:
      400:
        description: "Invalid input"
    defintions:
      CreatePostRequest:
        type: "object"
        properties:
          subject:
            type: "string"
          content:
            type: "string"
          public:
            type: "boolean"
          tags:
            type: "[string]"
    """
#securityDefinitions:
#      tokenauth:
#        type: apiKey
#        in: header
#        name: TIL-API-TOKEN


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
    """ Get all public posts
    ---
    tags: posts
    parameters:
      - name: author_id
        in: query
        description: Get posts by an author
        type: integer
    responses:
      200:
        description: Lists of posts
        schema:
          type: array
          $ref: "#/definitions/PostResponse"
    definitions:
      PostResponse:
        type: "array"
        items:
          subject:
            type: "string"
          content:
            type: "string"
          public:
            type: "boolean"
          tags:
            type: "[string]"
          author_id:
            type: "integer"
          post_date:
            type: "string"
    """
    posts = Post.query
    author_id = request.query.args.get('author_id')
    if author_id:
        posts = posts.filter_by(author_id=author_id).all()
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
    app.run(port=5001)
