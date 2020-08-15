# gathory


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

For more information read this:

https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api
