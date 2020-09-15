# This module tests to see APIs that relates to users works correctly or not
# NOTE: This test should not be used in production server
# (Due to generating random user in DB)
# TODO: Make test to be usable in production server
import json
import random
import string

# Load config file
with open('config.json', mode='r') as config_file:
    CONFIG = json.load(config_file)
HEADERS = {
    'Content-Type': 'application/json'
}
TOKEN = ""


def generate_random_string(length):
    """
    For generating random username
    """
    result_str = ''.join(
        random.choice(string.ascii_lowercase) for i in range(length)
    )
    return result_str


USERNAME = f'test_{generate_random_string(8)}'
PASSWORD = "test"


def test_create_random_user_accepted(app, client):
    """
    curl -i -H "Content-Type: application/json" -X POST
    -d '{"username": "RANDOM", "password": "test"}' localhost:5000/signup
    """

    data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    res = client.post(
        CONFIG.get('routes', {}).get('user', {}).get('signup'),
        data=json.dumps(data),
        headers=HEADERS
    )

    assert res.status_code == 200


def test_create_random_user_failed(app, client):
    data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    res = client.post(
        CONFIG.get('routes', {}).get('user', {}).get('signup'),
        data=json.dumps(data),
        headers=HEADERS
    )

    assert res.status_code == 403


def test_login_accepted(app, client):
    """
    curl -i -H "Content-Type: application/json" -X POST
    -d '{"username": "user1", "password": "zanjan"}' localhost:5000/login
    """

    data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    res = client.post(
        CONFIG.get('routes', {}).get('user', {}).get('login'),
        data=json.dumps(data),
        headers=HEADERS
    )

    global TOKEN
    TOKEN = json.loads(res.get_data(as_text=True))["access_token"]
    assert res.status_code == 200


def test_login_failed(app, client):
    data = {
        "username": "USER_THAT_DOESNT_EXISTS",
        "password": PASSWORD
    }
    res = client.post(
        CONFIG.get('routes', {}).get('user', {}).get('login'),
        data=json.dumps(data),
        headers=HEADERS
    )
    assert res.status_code == 401


def test_get_list_failed(app, client):
    """
    No link exists now!
    curl -H "Authorization: Bearer TOKEN" http://localhost:5000/links
    """

    headers = {
        'Authorization': f"Bearer {TOKEN}"
    }

    res = client.get(
        CONFIG.get('routes', {}).get('user', {}).get('links'),
        headers=headers
    )
    assert res.status_code == 404


def test_append_link_valid_data_accepted(client):
    """
    curl -i -H "Content-Type: application/json"
    -X POST -H "Authorization: Bearer $x"
    -d '{"url": "https://google.com","categories": ["search", "google"]}'
    http://localhost:5000/user/links
    """

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {
        "url": "https://google.com",
        "categories": ["search", "google"]
    }

    res = client.post(
        CONFIG.get('routes', {}).get('user', {}).get('links'),
        headers=headers,
        data=json.dumps(data)
    )
    assert res.status_code == 200


def test_get_list_accepted(app, client):
    """
    No link exists now!
    curl -H "Authorization: Bearer TOKEN" http://localhost:5000/links
    """

    headers = {
        'Authorization': f"Bearer {TOKEN}"
    }

    res = client.get(
        CONFIG.get('routes', {}).get('user', {}).get('links'),
        headers=headers
    )
    assert res.status_code == 200


def test_append_link_invalid_data_rejected(client):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {
        "url": "test.com",
        "categories": ["1", "2", "3"]
    }

    res = client.post(
        CONFIG.get('routes', {}).get('user', {}).get('links'),
        headers=headers,
        data=json.dumps(data)
    )
    assert res.status_code == 400
