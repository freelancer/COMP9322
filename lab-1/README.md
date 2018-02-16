# Lab 1 - Implement an Authentication service

## Goal

Create a HTTP API backend for handling user management (**auth** service)

The goal of this lab is to implement a HTTP API to perform the 
following functionalities:

- User signup
- User login
- User login check
- Respond to queries for user details

We will be using this service in [Lab 2](../lab-2) where we implement a web application which requires user signup/login
functionalities.

## Implementation

We will use Python 3.5+ and the following third party packages:

- [flask](flask.pocoo.org/docs/0.12/appcontext/#app-context)
- [flask-sqlalchemy](https://flask-sqlalchemy.pocoo.org)
- [flask-migrate](https://flask-migrate.readthedocs.io/en/latest/)
- [werkzeug](http://werkzeug.pocoo.org/)
- [flasgger](https://github.com/rochacbruno/flasgger)

The `src/` directory has the source for the entire application. The key files are:

- `models.py`: This defines the data models for the application
- `app.py`: The Flask application which is the HTTP server
- `config.py`: This has a `SECRET_KEY` which is used to generate auth tokens. This should be something more
  sensible and protected in a real life scenario

The database we use is [sqlite](https://docs.python.org/3/library/sqlite3.html) which is easy to setup
and we don't need to worry about setting up a real SQL server. In addition, all our code will continue
to work when we switch to a real MySQL server.

### A note on the authentication model

When a user logs in, they are sent back an `auth token` which should then be passed on to subsequent requests that requires
a valid auth token. The token generated is time limited to 10 minutes. You can change it by modifying the code in [models.py](./src/models.py). The server doesn't keep a record of the token which is an example of a stateless auth token. The
expiration information is completely embedded in the token itself. 

## Running the sample service

We will need Python 3.5+ and `pip` installed. Install [pipenv](https://docs.pipenv.org):

```
$ pip3 install pipenv
```

Setup application environment:

```
$ <GIT REPO HOME>
$ cd lab-1
$ pipenv install
```

For the first time, we will need to create the DB which is a `sqlite` DB:

```
$ cd src
$ FLASK_APP=app.py pipenv run flask db init
$ FLASK_APP=app.py pipenv run flask db migrate
$ FLASK_APP=app.py pipenv run flask db upgrade
```


Run application:

```
$ <repo root>
$ cd lab-1/src
$ pipenv run python app.py
```

## Viewing the API documentation

Once the application is up and running, go to `http://127.0.0.1:5000/apidocs/` to see the API docs and
even make sample requests.


## Using the service

We can make HTTP API requests to the service using a HTTP client like [postman](https://www.getpostman.com/),
`curl` or a more a friendlier command line client [httpie](https://httpie.org/). The following are examples
using `httpie`:

Signup a new user:

```
$ http POST 127.0.0.1:5000/users/signup/ username=user3 email=user@user2.com password=hello first_name=User last_name=Name
...
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
..

```


## Development

### Change any DB model

If we change any model, any changes to model:

```
$ FLASK_APP=app.py pipenv run flask db migrate
$ FLASK_APP=app.py pipenv run flask db upgrade
```

Add the changes to version control.

### Add new dependency

To add a new dependency:

```
$ pipenv install <dep name>
```

Commit the updated files
