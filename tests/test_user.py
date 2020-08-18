# This module tests to see login API works correctly or not
import json

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
    res = client.post("/login", data=json.dumps(data), headers=headers)
    #res = client.get('/')
    assert res.status_code == 200
    #expected = {'hello': 'world'}
    #assert expected == json.loads(res.get_data(as_text=True))


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
    res = client.post("/login", data=json.dumps(data), headers=headers)
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
    res = client.post("/signup", data=json.dumps(data), headers=headers)
    assert res.status_code == 200