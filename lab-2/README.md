# Lab 2 - Today I Learned HTTP service

## Goal

Create a HTTP API backend for a "Today I learned" application

The goal of this lab is to implement a HTTP API to perform the 
following functionalities:

- Create new posts
- Retreive posts

To perform the functionality of user management, we will use the user management
service we implemented in [lab 1](../lab-1). To interact with the `til` service, 
a user will need to have an account which they will sign up by interacting with the
`user management` service.
                                                                                                              
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
$ FLASK_APP=app.py pipenv run flask db init
$ FLASK_APP=app.py pipenv run flask db migrate
$ FLASK_APP=app.py pipenv run flask db upgrade
```

If we change any model, any changes to model:


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

