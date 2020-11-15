# This module tests to see APIs that relates to users works correctly or not
# NOTE: This test should not be used in production server
# (Due to generating random user in DB)
# TODO: Make test to be usable in production server
import json
import random
import string


def generate_random_string(length: int) -> str:
    """
    For generating random username
    """
    result_str = ''.join(
        random.choices(string.ascii_lowercase, k=length)
    )
    return result_str


USERNAME = f'test_{generate_random_string(8)}'
PASSWORD = 'test'

# Load config file
with open('config.json', mode='r') as config_file:
    CONFIG = json.load(config_file)
HEADERS = {
    'Content-Type': 'application/json'
}
# Routes
USER_SIGNUP_ROUTE = CONFIG.get('routes', {}).get('user', {}).get('signup')
USER_LOGIN_ROUTE = CONFIG.get('routes', {}).get('user', {}).get('login')
LINKS_MAIN_ROUTE = CONFIG.get('routes', {}).get('links', {}).get('main')
CATEGORIES_MAIN_ROUTE = CONFIG.get(
    'routes', {}).get('categories', {}).get('main')
LINKS_BY_CATEGORY_ROUTE = CONFIG.get(
    'routes', {}).get('links', {}).get('by_category')
LINKS_BY_SEARCH_ROUTE = CONFIG.get(
    'routes', {}).get('links', {}).get('by_pattern')

TOKEN = ""
NEW_CREATED_LINK_ID = ""
NEW_CREATED_CATEGORY_ID = ""


def test_create_random_user_accepted(app, client):
    """
    curl -i -H "Content-Type: application/json" -X POST
    -d '{"username": "RANDOM", "password": "test"}' localhost:5000/user/signup
    """

    data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    res = client.post(
        USER_SIGNUP_ROUTE,
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
        USER_SIGNUP_ROUTE,
        data=json.dumps(data),
        headers=HEADERS
    )

    assert res.status_code == 403


def test_login_accepted(app, client):
    """
    curl -i -H "Content-Type: application/json" -X POST
    -d '{"username": "user1", "password": "zanjan"}' localhost:5000/user/login
    """

    data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    res = client.post(
        USER_LOGIN_ROUTE,
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
        USER_LOGIN_ROUTE,
        data=json.dumps(data),
        headers=HEADERS
    )
    assert res.status_code == 401


def test_get_list_failed(app, client):
    """
    No link exists now!
    curl -H "Authorization: Bearer TOKEN" http://localhost:5000/links/get
    """

    headers = {
        'Authorization': f"Bearer {TOKEN}"
    }

    res = client.get(
        LINKS_MAIN_ROUTE,
        headers=headers
    )
    assert res.status_code == 404


def test_add_link_valid_data_accepted(client):
    """
    curl -i -H "Content-Type: application/json"
    -X POST -H "Authorization: Bearer $x"
    -d '{"url": "https://google.com","categories": ["search", "google"]}'
    http://localhost:5000/user/links/add
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
        LINKS_MAIN_ROUTE,
        headers=headers,
        data=json.dumps(data)
    )
    global NEW_CREATED_LINK_ID
    NEW_CREATED_LINK_ID = json.loads(res.get_data(as_text=True))["id"]
    assert res.status_code == 200


def test_add_link_valid_data_without_category_accepted(client):
    """
    curl -i -H "Content-Type: application/json"
    -X POST -H "Authorization: Bearer $x"
    -d '{"url": "https://google.com"}'
    http://localhost:5000/user/links/add
    """

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {
        "url": "https://google.com"
    }

    res = client.post(
        LINKS_MAIN_ROUTE,
        headers=headers,
        data=json.dumps(data)
    )
    assert res.status_code == 200


def test_get_list_accepted(app, client):
    """
    No link exists now!
    curl -H "Authorization: Bearer TOKEN" http://localhost:5000/links/get
    """

    headers = {
        'Authorization': f"Bearer {TOKEN}"
    }

    res = client.get(
        LINKS_MAIN_ROUTE,
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
        LINKS_MAIN_ROUTE,
        headers=headers,
        data=json.dumps(data)
    )
    assert res.status_code == 400


def test_get_link_by_id_accepted(client):
    """curl -i -H "Authorization: Bearer $x" -X GET localhost:5000/links/get/24
    """
    headers = {
        'Authorization': f"Bearer {TOKEN}"
    }
    res = client.get(
        f'{LINKS_MAIN_ROUTE}/{NEW_CREATED_LINK_ID}',
        headers=headers
    )
    assert res.status_code == 200


def test_get_categories_accepted(client):
    """curl -i -H "Authorization: Bearer $x"
    -X GET localhost:5000/categories"""
    headers = {
        'Authorization': f"Bearer {TOKEN}"
    }
    res = client.get(
        CATEGORIES_MAIN_ROUTE,
        headers=headers
    )
    global NEW_CREATED_CATEGORY_ID
    NEW_CREATED_CATEGORY_ID = json.loads(res.get_data(as_text=True))[-1]['id']
    assert res.status_code == 200


def test_get_category_by_id_accepted(client):
    """curl -i -H "Authorization: Bearer $x" -X GET localhost:5000/categories/6
    """
    headers = {
        'Authorization': f"Bearer {TOKEN}"
    }
    res = client.get(
        f'{CATEGORIES_MAIN_ROUTE}/{NEW_CREATED_CATEGORY_ID}',
        headers=headers
    )
    assert res.status_code == 200


def test_get_category_by_id_rejected(client):
    """curl -i -H "Authorization: Bearer $x" -X GET localhost:5000/categories/6
    """
    headers = {
        'Authorization': f"Bearer {TOKEN}"
    }
    res = client.get(
        f'{CATEGORIES_MAIN_ROUTE}/{NEW_CREATED_CATEGORY_ID+1}',
        headers=headers
    )
    assert res.status_code == 404


def test_get_link_by_category_id_accepted(client):
    """curl -i -H "Authorization: Bearer $x"
    -X GET localhost:5000/links/category/22"""
    headers = {
        'Authorization': f"Bearer {TOKEN}"
    }
    res = client.get(
        f'{LINKS_BY_CATEGORY_ROUTE}/{NEW_CREATED_CATEGORY_ID}',
        headers=headers
    )
    assert res.status_code == 200


def test_get_links_by_search_valid_data_accepted(client):
    """curl -i -H "Authorization: Bearer $x"
    -X GET localhost:5000/links/search/"test" """
    headers = {
        'Authorization': f"Bearer {TOKEN}"
    }
    res = client.get(
        f'{LINKS_BY_SEARCH_ROUTE}/google',
        headers=headers
    )
    assert res.status_code == 200


def test_get_links_by_search_invalid_data_rejected(client):
    """curl -i -H "Authorization: Bearer $x"
    -X GET localhost:5000/links/search/"test" """
    headers = {
        'Authorization': f"Bearer {TOKEN}"
    }
    res = client.get(
        f'{LINKS_BY_SEARCH_ROUTE}/NOT_vAlId_DaTa',
        headers=headers
    )
    assert res.status_code == 404


def test_get_link_by_category_id_invalid_data_rejected(client):
    """curl -i -H "Authorization: Bearer $x"
    -X GET localhost:5000/links/category/22"""
    headers = {
        'Authorization': f"Bearer {TOKEN}"
    }
    res = client.get(
        f'{LINKS_BY_CATEGORY_ROUTE}/{NEW_CREATED_CATEGORY_ID+1}',
        headers=headers
    )
    assert res.status_code == 404


def test_delete_link_by_id_accepted(client):
    """curl -i -H "Content-Type: application/json"
    -H "Authorization: Bearer $x" -X DELETE localhost:5000/user/links/16
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    res = client.delete(
        f'{LINKS_MAIN_ROUTE}/{NEW_CREATED_LINK_ID}',
        headers=headers
    )
    assert res.status_code == 200


def test_get_link_by_id_failed(client):
    """
    NO ID EXISTS NOW BECAUSE OF PREVIOUS CALL
    """
    headers = {
        'Authorization': f"Bearer {TOKEN}"
    }
    res = client.get(
        f'{LINKS_MAIN_ROUTE}/{NEW_CREATED_LINK_ID}',
        headers=headers
    )
    assert res.status_code == 404


def test_delete_link_by_id_failed(client):
    """
    NO ID EXISTS NOW BECAUSE OF PREVIOUS CALL
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    res = client.delete(
        f'{LINKS_MAIN_ROUTE}/{NEW_CREATED_LINK_ID}',
        headers=headers
    )
    assert res.status_code == 404
