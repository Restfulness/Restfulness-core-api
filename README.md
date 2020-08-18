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

#### Tests

Something that is untested is broken!
To run tests, make sure you are in root directory of the project (the directory that contains `api.py` file) then run:
```
python -m pytest
```

For more information read this:

* https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api
* https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage
* https://python-jsonschema.readthedocs.io/en/stable/
* https://flask.palletsprojects.com/en/1.1.x/testing/
* http://sqlalchemy.org/
