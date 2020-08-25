# This module tests to see APIs that relates to users works correctly or not
import json

# Load config file
with open('config.json', mode='r') as config_file:
    CONFIG = json.load(config_file)

HEADERS = {
    'Content-Type': 'application/json'
}

TOKEN = ""


def test_login_successful(app, client):
    """
    curl -i -H "Content-Type: application/json" -X POST
    -d '{"username": "user1", "password": "zanjan"}' localhost:5000/login
    """

    data = {
        "username": "user1",
        "password": "zanjan"
    }
    res = client.post(
        CONFIG['routes']['user']['login'], data=json.dumps(data),
        headers=HEADERS
    )
    global TOKEN
    TOKEN = json.loads(res.get_data(as_text=True))["access_token"]
    assert res.status_code == 200


def test_get_list(app, client):
    """
    curl -H "Authorization: Bearer TOKEN" http://localhost:5000/links
    """

    headers = {
        'Authorization': f"Bearer {TOKEN}"
    }

    res = client.get(CONFIG['routes']['user']['links'], headers=headers)
    assert res.status_code == 200


def test_append_link(client):
    """
    curl -i -H "Content-Type: application/json" -H "Authorization: Bearer $x"
    -X POST -d '{"address_name": "test.com", "categories": ["1", "2", "3"]}'
    http://localhost:5000/user/links
    """

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {
        "address_name": "test.com",
        "categories": ["1", "2", "3"]
    }
    res = client.post(CONFIG['routes']['user']['links'], headers=headers,
                      data=json.dumps(data))
    assert res.status_code == 200


def test_delete_link(client):
    """
    curl -i -H "Content-Type: application/json" -H "Authorization: Bearer $x"
    -X DELETE -d '{"address_name": "test.com"}' localhost:5000/user/links
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {
        "address_name": "test.com"
    }

    res = client.delete(CONFIG['routes']['user']['links'], headers=headers,
                        data=json.dumps(data))
    assert res.status_code == 200


def test_login_failed(app, client):
    """
    curl -i -H "Content-Type: application/json" -X POST
    -d '{"username": "xxxx", "password": "yyyy"}' localhost:5000/login
    """

    data = {
        "username": "xxxx",
        "password": "yyyy"
    }
    res = client.post(
        CONFIG['routes']['user']['login'], data=json.dumps(data),
        headers=HEADERS
    )
    assert res.status_code == 401


def test_create_user(app, client):
    """
    curl -i -H "Content-Type: application/json" -X POST
    -d '{"username": "farbod", "password": "zanjan"}' localhost:5000/signup
    """

    data = {
        "username": "ali",
        "password": "1234"
    }
    res = client.post(
        CONFIG['routes']['user']['signup'], data=json.dumps(data),
        headers=HEADERS
    )
    assert res.status_code == 200
