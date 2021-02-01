from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

import json
import random
import string

with open('config.json', mode='r') as config_file:
    CONFIG = json.load(config_file)

HEADERS = {
    'Content-Type': 'application/json'
}

# Routes
USER_SIGNUP_ROUTE = CONFIG.get('routes', {}).get('user', {}).get('signup')
USER_LOGIN_ROUTE = CONFIG.get('routes', {}).get('user', {}).get('login')
USER_FORGET_PASSWORD = CONFIG.get('routes', {}).get('user', {}).get(
    'forget_password')
USER_VERIFY_CODE = CONFIG.get('routes', {}).get('user', {}).get('verify_code')
USER_RESET_PASSWORD = CONFIG.get('routes', {}).get('user', {}).get(
    'reset_password')
USER_PROFILE_ROUTE = CONFIG.get('routes', {}).get('user', {}).get(
    'profile')


def generate_random_string(length):
    """
    For generating random username
    """
    result_str = ''.join(random.choices(string.ascii_lowercase, k=length))
    return result_str


def get_valid_code_from_hashed_data(hashed_data: str) -> str:
    """ Returns valid 8 digit code from hashed returned by server"""
    hash = Serializer(CONFIG.get('forget_password', {}).
                      get('serializer_secret_key'))
    try:
        data = hash.loads(hashed_data)
    except SignatureExpired:
        raise
    except BadSignature:
        raise

    return(data['valid_code'])


USERNAME = f'test_{generate_random_string(8)}@gmail.com'
CURRENT_PASSWORD = 'test'
NEW_PASSWORD = 'test_test'
HASHED_DATA_FROM_SERVER = ''
RESET_PASSWORD_TOKEN = ''


def test_create_random_user_accepted(app, client):
    """
    curl -i -H "Content-Type: application/json" -X POST
    -d '{"username": "RANDOM", "password": "test"}' localhost:5000/user/signup
    """

    data = {
        "username": USERNAME,
        "password": CURRENT_PASSWORD,
        "email": f'{USERNAME}@gmail.com'
    }
    res = client.post(
        USER_SIGNUP_ROUTE,
        data=json.dumps(data),
        headers=HEADERS
    )

    assert res.status_code == 200


def test_login_with_first_password_accepted(app, client):
    """
    curl -i -H "Content-Type: application/json" -X POST
    -d '{"username": "user1", "password": "zanjan"}' localhost:5000/user/login
    """

    data = {
        "username": USERNAME,
        "password": CURRENT_PASSWORD
    }
    res = client.post(
        USER_LOGIN_ROUTE,
        data=json.dumps(data),
        headers=HEADERS
    )

    assert res.status_code == 200


def test_request_forget_password_code_accepted(client):
    """
    curl -i -H "Content-Type: application/json"
    -X POST -d '{"username": "farbod"}' localhost:5000/user/password/forget
    """
    data = {
        "username": USERNAME
    }
    res = client.post(
        USER_FORGET_PASSWORD,
        data=json.dumps(data),
        headers=HEADERS
    )

    global HASHED_DATA_FROM_SERVER
    HASHED_DATA_FROM_SERVER = json.loads(
        res.get_data(as_text=True))['hashed_data']
    assert res.status_code == 200


def test_request_forget_password_code_invalid_user_failed(client):
    """
    curl -i -H "Content-Type: application/json"
    -X POST -d '{"username": "farbod"}' localhost:5000/user/password/forget
    """
    data = {
        "username": 'INVALID_USERNAME'
    }
    res = client.post(
        USER_FORGET_PASSWORD,
        data=json.dumps(data),
        headers=HEADERS
    )

    assert res.status_code == 404


def test_verify_code_accepted(client):
    """
    curl -i -H "Content-Type: application/json" -X POST
    -d '{"hashed_data": "eyJ...", "user_input": 68756412}'
    localhost:5000/user/password/verify
    """
    data = {
        "hashed_data": HASHED_DATA_FROM_SERVER,
        "user_input": get_valid_code_from_hashed_data(HASHED_DATA_FROM_SERVER)
    }
    res = client.post(
        USER_VERIFY_CODE,
        data=json.dumps(data),
        headers=HEADERS
    )

    global RESET_PASSWORD_TOKEN
    RESET_PASSWORD_TOKEN = json.loads(
        res.get_data(as_text=True))['reset_password_token']
    assert res.status_code == 200


def test_verify_code_invalid_code_rejected(client):
    data = {
        "hashed_data": HASHED_DATA_FROM_SERVER,
        "user_input": '111'
    }
    res = client.post(
        USER_VERIFY_CODE,
        data=json.dumps(data),
        headers=HEADERS
    )

    assert res.status_code == 400


def test_verify_code_invalid_token_rejected(client):
    data = {
        "hashed_data": 'INVALID_TOKEN',
        "user_input": get_valid_code_from_hashed_data(HASHED_DATA_FROM_SERVER)
    }
    res = client.post(
        USER_VERIFY_CODE,
        data=json.dumps(data),
        headers=HEADERS
    )

    assert res.status_code == 401


def test_reset_password_accepted(client):
    """
    curl -i -H "Content-Type: application/json" -X POST
    -d '{"reset_password_token": "eyJhb...", "new_password": "test"}'
    localhost:5000/user/password/reset
    """
    data = {
        "reset_password_token": RESET_PASSWORD_TOKEN,
        "new_password": NEW_PASSWORD
    }
    res = client.post(
        USER_RESET_PASSWORD,
        data=json.dumps(data),
        headers=HEADERS
    )

    assert res.status_code == 200


def test_reset_password_invalid_token_rejected(client):
    data = {
        "reset_password_token": 'INVALID_TOKEN',
        "new_password": NEW_PASSWORD
    }
    res = client.post(
        USER_RESET_PASSWORD,
        data=json.dumps(data),
        headers=HEADERS
    )

    assert res.status_code == 401


def test_login_with_first_password_failed(client):
    data = {
        "username": USERNAME,
        "password": CURRENT_PASSWORD
    }
    res = client.post(
        USER_LOGIN_ROUTE,
        data=json.dumps(data),
        headers=HEADERS
    )

    assert res.status_code == 401


def test_login_with_new_password_accepted(client):
    data = {
        "username": USERNAME,
        "password": NEW_PASSWORD
    }
    res = client.post(
        USER_LOGIN_ROUTE,
        data=json.dumps(data),
        headers=HEADERS
    )

    global TOKEN
    TOKEN = json.loads(res.get_data(as_text=True))["access_token"]
    assert res.status_code == 200


def test_delete_user_profile_accepted(client):
    """curl -i -H "Content-Type: application/json" -H "Authorization: Bearer $x"
    -X DELETE localhost:5000/user/profile
    """
    headers = {
        'Authorization': f"Bearer {TOKEN}"
    }
    res = client.delete(
        USER_PROFILE_ROUTE,
        headers=headers
    )

    assert res.status_code == 200
