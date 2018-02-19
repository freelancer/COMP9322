# Lab 2 - Today I Learned HTTP service

## Goal

Create a HTTP API backend for a "Today I learned" application. The application is meant to provide
a platform for users to create short posts (upto 800 characters) on what they learn everyday.
Each post has a subject, body and one or more tags associated with them. In addition, each post can either
be marked private (default) or be public. Private posts are only visible to their creators. Users need to have
a valid account to be able to create posts.

The goal of this lab is to implement a HTTP API to perform the 
following functionalities:

- Create new posts
- Retreive posts

To perform the functionality of user management, we will use the user management
service we implemented in [lab 1](../lab-1). To interact with the `til` service, 
a user will need to have an account which they will sign up by interacting with the
`user management` service. For functionalities which require the user to have a valid
auth token, they will supply the token via the `TIL-API-TOKEN` HTTP header.

The interaction between the TIL HTTP API backend and the user management service can roughly
be represented as follows:
                                                                                                              
                         .─────────.                                                      .─────────.         
                        ╱           ╲                                                    ╱           ╲        
                       (User Database)                                                  (TIL Database )       
                        `.         ,'                                                    `.         ,'        
                          `───────'                                                        `───────'          
                              ▲                                                                ▲              
                              │                                                                │              
                              │                                                                │              
                              │                                                                ▼              
                              ▼                                                   ┌──────────────────────────┐
                  ┌─────────────────────────┐                                     │     Today I Learned      │
                  │                         │              HTTP                   │                          │
                  │ User Management Service │    ◀────────────────────────        │         HTTP API         │
                  │                         │                                     │                          │
                  │                         │    User supplied a valid token?     │                          │
                  └─────────────────────────┘                                     └──────────────────────────┘
                                                                                                              
                               ▲                                                               ▲              
                               │                                                               │              
                               │                                                               │              
                               │                                                               │              
                               │                                                               │              
                     ┌────────────────────┐                                          ┌────────────────────┐   
                     │  HTTP client/user  │                                          │  HTTP client/user  │   
                     └────────────────────┘                                          └────────────────────┘   



## Implementation

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
$ http POST 127.0.0.1:5001/posts/ TIL-API-Token:'{"user_id": 1}.DWv1wQ.I-6pyv5yFfEnY7MC5bWhUwL
ygjA'  subject="Hello World" content="Hello there; this is my first post" tags='["updates", "python"]'
HTTP/1.0 200 OK
Content-Length: 19
Content-Type: application/json
Date: Mon, 19 Feb 2018 05:49:17 GMT
Server: Werkzeug/0.14.1 Python/3.5.3

{
    "post_id": 1
}
```

**Retrieving posts**

```
$ http 127.0.0.1:5001/posts/?author_id=3 TIL-API-TOKEN:'{"user_id": 1}.DWv7Ug._tyipTRCoF8JqX25
KwO8XaYw4DI'
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

