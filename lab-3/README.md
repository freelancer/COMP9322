# Lab 3 - Simple analytics for Today I Learned HTTP service

## Goal

In this lab, we expand [Lab -2](../lab-2) to implement basic analytics service. In Lab 2, we implemented 
support for retrieving all the current tags. However, let's say we want to be able to see the tags that 
are most used. Although we could do SQL queries to the database to fetch this information, we will unncessarily
burden the database for such requests. In addition, imagine thousands and millions of user creating posts
with tags and you always want to know what are the top N tags in your application. To implement this feature,
we will use a popular datastore, [redis](https://redis.io/). More specifically, we will use a redis feature
called [sorted sets](http://echorand.me/sorted-sets-in-redis-from-cli-python-and-golang.html).


## Implementation

We will use Python 3.5+ and the following third party packages:

- [flask](flask.pocoo.org/docs/0.12/appcontext/#app-context)
- [flask-sqlalchemy](https://flask-sqlalchemy.pocoo.org)
- [flask-migrate](https://flask-migrate.readthedocs.io/en/latest/)
- [werkzeug](http://werkzeug.pocoo.org/)
- [flasgger](https://github.com/rochacbruno/flasgger)
- [requests](http://docs.python-requests.org/en/master/)
- [redis](https://pypi.python.org/pypi/redis)

The `src/` directory has the source for the entire application. The key files are:

- `models.py`: This defines the data models for the application
- `app.py`: The Flask application which is the HTTP server

The database we use is [sqlite](https://docs.python.org/3/library/sqlite3.html) which is easy to setup
and we don't need to worry about setting up a real SQL server. In addition, all our code will continue
to work when we switch to a real MySQL server.

The source is a copy of our code in lab 2 with the following additions to `app.py`:

- Add a new endpoint: `/tags/top/`
- After each new post, the tag counter is updated by calling `redis`.

## Running the sample service

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
$ FLASK_APP=app.py pipenv run flask db upgrade
```

Run application:

```
$ <repo root>
$ cd lab-2/src
$ pipenv run python app.py
```

We also need to have a local `redis` server running. Please see the [documentation](https://redis.io/download)
on how you can download redis and run it.

## Viewing the API documentation 

Once the application is up and running, go to `http://127.0.0.1:5001/apidocs/` to see the API docs and
even make sample requests.


## Using the service

The first step to use the service is to have a valid user token which we can obtain as shown in [lab 1](../lab-1)
and then pass that as a header with requests we make to the service.

**Sign up and Get a authentication token**

We will do so by making an API request to the user management service:

```
$  http POST 127.0.0.1:5000/users/signup/ username=amitsaha email=asah@freelancer.com password
=secret first_name=Amit last_name=Saha
HTTP/1.0 200 OK
Content-Length: 19
Content-Type: application/json
Date: Mon, 19 Feb 2018 05:43:47 GMT
Server: Werkzeug/0.14.1 Python/3.5.3

{
    "user_id": 1
}
```

Now that we have created an account, let's get an auth token:

```
$ http POST 127.0.0.1:5000/users/login/ username=amitsaha password=secret
HTTP/1.0 200 OK
Content-Length: 49
Content-Type: text/html; charset=utf-8
Date: Mon, 19 Feb 2018 05:44:33 GMT
Server: Werkzeug/0.14.1 Python/3.5.3

{"user_id": 1}.DWv1wQ.I-6pyv5yFfEnY7MC5bWhUwLygjA
```

The response is the entire auth token and is valid for 10 minutes.


**Creating a new post**

Next, we will create a new post supplying the above auth token:

```
$ http POST 127.0.0.1:5001/posts/ TIL-API-Token:'{"user_id": 1}.DWzv3A.RRwp-VfrpnpuXGyRuRYPm7PT4To'  subject="Hello World" content="Hello there; this is my first post" tags:='["ruby", "python"]'

HTTP/1.0 200 OK
Content-Length: 19
Content-Type: application/json
Date: Mon, 19 Feb 2018 05:49:17 GMT
Server: Werkzeug/0.14.1 Python/3.5.3

{
    "post_id": 1
}
```

Create a few more posts with different tags.

**Get top 5 tags**

```
$ http 127.0.0.1:5001/tags/top/
HTTP/1.0 200 OK
Content-Length: 26
Content-Type: application/json
Date: Tue, 20 Feb 2018 06:30:38 GMT
Server: Werkzeug/0.14.1 Python/3.6.3

[
    "python",
    "ruby"
]
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

