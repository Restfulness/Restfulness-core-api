# Flask Restfulness

Another boilerplate for flask-restful web service (Including flask-sqlalchemy, flask-jwt, Swagger, Docker, ...)

This project is going to be something like [Pocket](https://getpocket.com/) to save your favorite links.

Now you can save your favourite links, add category to them, return them by category or by looking
for some special keyword in their URL, ...

### Production Environment (Using Docker)

If you have `docker` and `docker-compose` installed, then simply you can run:
(Make sure you are in root directory of project which is folder that contains `api.py`)
```
docker-compose up
```
And that's it :) now you can open `http://localhost:5000/apidocs` to see available APIs.


(To run CI tests using `pytest` in this way, you can simply run `docker-compose run app python -m pytest`; But make sure to wait a few seconds for MySql to get ready)

By default, our `docker-compose` configuration will disables `root`'s password for `MySql` after initialization; So app connects to `restfulness` database with `test` user which is created using enviromental variables in `docker-compose.yml` file. If you want to changes this setting, make
sure to read [MySql Docker Documentation](https://hub.docker.com/_/mysql), then change `docker-compose.yml` and `config.json` correctly.

**Note:** By default, Database is persistent using [Docker Volumes](https://docs.docker.com/storage/volumes/), so you don't need to worry about losing your data *unless* you turn off everything using `docker-compose down -v` command. To make a long story short and for more information, take a look
at [this](https://stackoverflow.com/a/39208187/5229664).


### Development Environment (Without Docker)

At the very beginning, you have to initiate a virtual environment with this:

```
sudo apt install -y python3-venv
python3 -m venv venv
```

And then every time that you want to run it:

```
source venv/bin/activate
python -m pip install -r requirements.txt
```

Then you can run

```
python api.py
```

##### Database Connection

This project supports both `MySql` and `SQLite` as its database.

By default, this code uses `MySql` as its main database but if you want to use `SQLite` (which is placed in `tests/test.db`) for testing purposes, make sure to change `mysql` option to `false` in `config.json`.

Else, if you want to continue using `MySql`, please follow instructions below:

Before running `api.py`, make sure you have `mysql server` installed and change db connection in
`config.json`.

To install `mysql server` in Debian based distributions you can run:

```
sudo apt install mysql-server
sudo mysql_secure_installation
```

Now change `username`, `password` and `db` in `config.json` to make the app able to connect
to database.


### Config.json
Before running the app, make sure to check all values in `config.json` file.
Default values are:
_reset password token expire time_ = 300 seconds

_verify random code token expire time_ = 300 seconds

_reset password code length_ = 8


### Tests

Something that is untested is broken!
To run tests, make sure you are in root directory of the project (the directory that contains `api.py` file) then run:
```
python -m pytest
```

### API Documentation
To see available APIs, go to http://localhost:5000/apidocs
(We are using [Flasgger](https://github.com/flasgger/flasgger) for our API's documentation)


### Clients
- [Restfulness Flutter App](https://github.com/Restfulness/Restfulness-flutter-app)


### Notes
- **How does reset password mechanism work?**
  1. Client sends a POST request to `/forget` endpoint, containing `user's username`.
  2. Server sends an 8 digit random created code to user's Email and returns a hash string which contains `User's ID, Valid 8 digit code and expire date`. (We use [ItsDangerous](https://itsdangerous.palletsprojects.com) for creating that hash, so it's safe.)
  3. Client sends a POST request to `/verify` endpoint, containing `user's entered 8 digit code` and `hash that was obtained from previous call`.
  4. Server returns a token for resetting password, **If** user entered the correct 8 digit code.
  5. At last, Client sends a POST request to `/reset` endpoint, containing `Reset password token that is obtained from previous call` and `user's new password`.
  6. For more information, read [this](https://dev.to/theanam/otp-verification-without-any-database-4ja5). (To make long story short, we do this to pick up unnecessary pressure from our server.)

For more information read this:

* https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api
* https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage
* https://python-jsonschema.readthedocs.io/en/stable/
* https://flask.palletsprojects.com/en/1.1.x/testing/
* http://sqlalchemy.org/
