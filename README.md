
## Introduction

In this project I set up a basic API to test CRUD operations for posts model, storing data in a PostrgeSQL Server deployed localy.

The API is developed with FLaskAPI. It connects to a PostgreSQL Server Database and creates 2 different tables: users and posts.
This tables are created by the API using ORM sqlAlchemy inheriting from BaseModel class. Its definitions can eb found in app/models.py. In this file it is also commented a definition of a model using SQLModel library.

On the other hand we create some schemas for body input and responses. They can be found at app/schemas.py

The API has different endpoints, to ernable basic CRUD operations. A user can create, update, list or delete posts. 
Security is implemented by login. A user must first login through the /login endpoint. Wityh correct credentials the user will obtain a JWT, which will have to use to contact endpoints.

Login logic is configured at app/oauth2.py.
The loogin flow is the following:

1. At /create_user endpoint a user creates its representation. Password is hashed and stored in users table algon with other parameters
2. User identifies at /login endpoint. At this endpoint, credentials provided are checked against the ones saved in the users table (hashed password). To hash and verify password functions in app/utils.py are used. Passlib library is used.
3. If credentials are matching, a JWT is returned. This JWT payload is created only with the user_id field, but copuld contain more fileds such as scopes. The token is encoded witha  secret value using jose.jwt
4. When a user tries for example to query for example /upload endpoint, through dependency token is required.


## Project structure:
At app/routers you will find a file for each group of endpoints. Authentication, posts and users. <br>
At app/models.py all the models defined using sqlAlchemy BaseModel.<br>
At app/schemas.py  all pydantic schemas.<br>
At app/oauth2.py all functions related to login flow<br>
At app/utils.py all utility functions.<br>
At app/main.py all routes are imported and FastAPI() instance is created.<br>


#### Future Work
Deploy the API in kubernetes
    - Build Dockerfile
    - Create env vars for some values
    - Create Helm Chart
    - Deploy the app as a package
Deploy PostgreSQL operator in minikube
Deploy PostreSQL cluster
    - Add manfiest to the Helm Chart?
Deploy Prometheus stack
Monitor with prometheus the application
    - Is instrumentation needed in the app?
    - Deploy ServiceMonitor object


