# Flask Restfulness


### Development Environment

At the very beginning, you have to initiate a virtual environment with this:

```
sudo apt-get install -y python3-venv
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

### Database Connection

Before running `api.py`, make sure you have `mysql server` installed and change db connection in
`config.json`.

To install `mysql server` in Debian based distributions you can run:

```
sudo apt install mysql-server
sudo mysql_secure_installation
```

Now change `username`, `password` and `db` in `config.json` to make the app able to connect
to database.

#### Tests

Something that is untested is broken!
To run tests, make sure you are in root directory of the project (the directory that contains `api.py` file) then run:
```
python -m pytest
```

#### API Documentation
To see available APIs, go to http://localhost:5000/apidocs
(We are using [Flasgger](https://github.com/flasgger/flasgger) for our API's documentation)


For more information read this:

* https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api
* https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage
* https://python-jsonschema.readthedocs.io/en/stable/
* https://flask.palletsprojects.com/en/1.1.x/testing/
* http://sqlalchemy.org/
