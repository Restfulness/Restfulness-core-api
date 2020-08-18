# This module tests to see APIs that relates to users works correctly or not
import json

# Load config file
with open('config.json', mode='r') as config_file:
    CONFIG = json.load(config_file)

TOKEN = ""
# curl -i -H "Content-Type: application/json" -X POST 
# -d '{"username": "user1", "password": "zanjan"}' localhost:5000/login
def test_login_successful(app, client):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "username": "user1",
        "password": "zanjan"
    }
    res = client.post(CONFIG['routes']['user']['login'], data=json.dumps(data), headers=headers)
    global TOKEN
    TOKEN = json.loads(res.get_data(as_text=True))["access_token"]
    assert res.status_code == 200


# curl -H "Authorization: Bearer TOKEN" http://localhost:5000/links
def test_get_list(app, client):
    headers = {
        'Authorization': f"Bearer {TOKEN}"
    }
    res = client.get(CONFIG['routes']['user']['links'], headers=headers)
    assert res.status_code == 200


# curl -i -H "Content-Type: application/json" -X POST 
# -d '{"username": "xxxx", "password": "yyyy"}' localhost:5000/login
def test_login_failed(app, client):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "username": "xxxx",
        "password": "yyyy"
    }
    res = client.post(CONFIG['routes']['user']['login'], data=json.dumps(data), headers=headers)
    assert res.status_code == 401


# curl -i -H "Content-Type: application/json" -X POST 
# -d '{"username": "farbod", "password": "zanjan"}' localhost:5000/signup
def test_create_user(app, client):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "username": "ali",
        "password": "1234"
    }
    res = client.post(CONFIG['routes']['user']['signup'], data=json.dumps(data), headers=headers)
    assert res.status_code == 200