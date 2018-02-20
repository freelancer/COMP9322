# Lab exercises for COMP9322

The overall goal of the following exercises is to demonstrate *service oriented architecture* or *microservices architecture*.
The general idea of this software design pattern is that each service performs a fairly indepedent role and multiple
services together offer one or more user facing functionality.

Our sample web application that we will use to demonstrate the above is a *Today I learned* application which is a
platform to write and share short posts about what users learn everyday. We will only focus on building the HTTP APIs
for each service and consider designing any Web User Interface as out of scope for these exercises. The interaction
with these services will be via HTTP clients.

## [Lab 1](./lab-1)

**Goal:** Create a HTTP API backend for handling user management (**auth** service)

- Handle user signup
- Handler user login (token based authentication)

## [Lab 2](./lab-2)

**Goal:** Create a HTTP API backend for the __Today I Learned__ application

- Create new posts
- View posts

## [Lab 3](./lab-3)

**Goal:** Implement basic analytics functionality for the __Today I learned__ application

- API endpoint to return top tags


## General notes

## Programming language

The programming language used for the exercises is *Python 3* and we will be using [pipenv](https://github.com/pypa/pipenv)
for using and managing third party packages.

### API Documentation

We will be using [Open API specification](https://swagger.io/docs/specification/about/) file for documenting our HTTP
API. The documentation will be added to the source as comments in the following form:

```python
""" New User Signup
    ---
    parameters:
      - in: "body"
        name: "body"
        description: "Signup a new User"
        required: true
        schema:
          $ref: "#/definitions/UserSignupRequest"
    responses:
      400:
        description: "Invalid input"
    definitions:
      UserSignupRequest:
        type: "object"
        properties:
          username:
            type: "string"
          first_name:
            type: "string"
          last_name:
            type: "string"
          email:
            type: "string"
          password:
            type: "string"
    """
    ...

```

Using [flasgger](https://github.com/rochacbruno/flasgger) when we run the service, the documentation will automatically become available to us at a desginated URL.
