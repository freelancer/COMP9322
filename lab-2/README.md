# Lab 2 - Today I Learned HTTP service

**Goal**

Create a HTTP API backend for a "Today I learned" application

The goal of this lab is to implement a HTTP API to perform the 
following functionalities:

- Create new posts
- Retreive posts

To perform the functionality of user management, we will use the user management
service we implemented in [lab 1](../lab-1).

**Implementation**

We will use Python 3.5+ and the following third party packages:

- [flask](flask.pocoo.org/docs/0.12/appcontext/#app-context)
- [flask-sqlalchemy](https://flask-sqlalchemy.pocoo.org)
- [flask-migrate](https://flask-migrate.readthedocs.io/en/latest/)
- [werkzeug](http://werkzeug.pocoo.org/)
- [flasgger](https://github.com/rochacbruno/flasgger)
- [requests](http://docs.python-requests.org/en/master/)

The `src/` directory has the source for the entire application. The key files are:

- `models.py`: This defines the data models for the application
- `app.py`: The Flask application which is the HTTP server

The database we use is [sqlite](https://docs.python.org/3/library/sqlite3.html) which is easy to setup
and we don't need to worry about setting up a real SQL server. In addition, all our code will continue
to work when we switch to a real MySQL server.


**Running the sample service**

We will need Python 3.5+ and `pip` installed. Install [pipenv](https://docs.pipenv.org):

```
$ pip3 install pipenv
```

Setup application environment:

```
$ <GIT REPO HOME>
$ cd lab-2
$ pipenv install
```

For the first time, we will need to create the DB which is a `sqlite` DB:

```
$ cd src
$ FLASK_APP=app.py pipenv run flask db init
$ FLASK_APP=app.py pipenv run flask db migrate
$ FLASK_APP=app.py pipenv run flask db upgrade
```

If we change any model, any changes to model:

```
$ FLASK_APP=app.py pipenv run flask db migrate
$ FLASK_APP=app.py pipenv run flask db upgrade
```

Run application:

```
$ <repo root>
$ cd lab-2/src
$ pipenv run python app.py
```

**Viewing the API documentation**

Once the application is up and running, go to `http://127.0.0.1:5000/apidocs/` to see the API docs and
even make sample requests.


**Using the service**

We can make HTTP API requests to the service using a HTTP client like [postman](https://www.getpostman.com/),
`curl` or a more a friendlier command line client [httpie](https://httpie.org/). The following are examples
using `httpie`:

Signup a new user:

```
$ http POST 127.0.0.1:5000/users/signup/ username=user3 email=user@user2.com password=hello first_name=User last_name=Name
```

Then, we can login using the above username and password:

```
$ http POST 127.0.0.1:5000/users/login/ username=user3 password=hello
< token >
```

The above request will return us a token which we can use to login or perform functionalities as
a logged in user:

```
$ http POST 127.0.0.1:5000/users/check/ token='{\"user_id\": 3}.DWKTqw.8GPHaqVKIwexvnWYOmxIu9uyMkw'
```

Query a user details:

```
$ http 127.0.0.1:5000/users/3/



```
Create a post:

```
$ http POST 127.0.0.1:6000/posts/ API-Token:"{\"user_id\": 1}.DWRiug.4Z9KsuYFEDRx27ucnFTjIFV0-wM" subject="Hello World" content="Hey hey" public=True tags:='["hello", "world"]'
```
