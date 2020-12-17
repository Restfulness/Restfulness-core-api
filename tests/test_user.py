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
# Routes
USER_SIGNUP_ROUTE = CONFIG.get('routes', {}).get('user', {}).get('signup')
USER_LOGIN_ROUTE = CONFIG.get('routes', {}).get('user', {}).get('login')
USER_PUBLICITY_ROUTE = CONFIG.get('routes', {}).get('user', {}).get(
    'publicity')
USER_ACTIVITY_ROUTE = CONFIG.get('routes', {}).get('user', {}).get(
    'activity_list')
LINKS_MAIN_ROUTE = CONFIG.get('routes', {}).get('links', {}).get('main')
CATEGORIES_MAIN_ROUTE = CONFIG.get(
    'routes', {}).get('categories', {}).get('main')
LINKS_BY_CATEGORY_ROUTE = CONFIG.get(
    'routes', {}).get('links', {}).get('by_category')
LINKS_BY_SEARCH_ROUTE = CONFIG.get(
    'routes', {}).get('links', {}).get('by_pattern')
LINKS_UPDATE_CATEGORY = CONFIG.get(
    'routes', {}).get('links', {}).get('update_category')
LINKS_BY_USER_ID = CONFIG.get(
    'routes', {}).get('links', {}).get('by_user_id')


TOKEN = ""
NEW_CREATED_LINK_ID = ""
NEW_CREATED_CATEGORY_ID = ""
NEW_CATEGORIES = ["test_1", "test_2"]
NEW_CREATED_USER_ID = ""
VALID_DATE = "2020-12-1 16:09"


def generate_random_string(length):
    """
    For generating random username
    """
    result_str = ''.join(
        random.choice(string.ascii_lowercase) for i in range(length)
    )
    return result_str


USERNAME = f'test_{generate_random_string(8)}@gmail.com'
PASSWORD = 'test'


def test_create_random_user_accepted(app, client):
    """
    curl -i -H "Content-Type: application/json" -X POST
    -d '{"username": "RANDOM", "password": "test"}' localhost:5000/user/signup
    """

    data = {
        "username":  USERNAME,
        "password": PASSWORD
    }
    res = client.post(
        USER_SIGNUP_ROUTE,
        data=json.dumps(data),
        headers=HEADERS
    )

    assert res.status_code == 200


def test_create_random_user_exists_failed(app, client):
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


def test_create_random_user_invalid_email_failed(app, client):
    data = {
        "username": "INVALID_EMAIL",
        "password": PASSWORD
    }
    res = client.post(
        USER_SIGNUP_ROUTE,
        data=json.dumps(data),
        headers=HEADERS
    )

    assert res.status_code == 400


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


def test_update_user_publicity_accepted(client):
    """url -i -H "Content-Type: application/json"
    -H "Authorization: Bearer $x" -X PUT
    -d '{"publicity": false}' localhost:5000/user/publicity
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }
    data = {
        'publicity': False
    }
    res = client.put(
        USER_PUBLICITY_ROUTE,
        data=json.dumps(data),
        headers=headers
    )
    assert res.status_code == 200


def test_get_user_publicity(client):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }
    res = client.get(
        USER_PUBLICITY_ROUTE,
        headers=headers
    )
    assert res.status_code == 200
    assert json.loads(res.get_data(as_text=True))['publicity'] is False


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


def test_get_link_by_pagination_accepted(client):
    """curl -i -H "Authorization: Bearer $x" -X GET
    "localhost:5000/links?page=100&page_size=2"
    """
    headers = {
        'Authorization': f"Bearer {TOKEN}"
    }
    res = client.get(
        f'{LINKS_MAIN_ROUTE}?page=1&page_size=2',
        headers=headers
    )
    assert res.status_code == 200


def test_get_link_by_pagination_not_found_rejected(client):
    headers = {
        'Authorization': f"Bearer {TOKEN}"
    }
    res = client.get(
        f'{LINKS_MAIN_ROUTE}?page=1000&page_size=2',
        headers=headers
    )
    assert res.status_code == 404


def test_get_link_by_pagination_exceed_limit_rejected(client):
    headers = {
        'Authorization': f"Bearer {TOKEN}"
    }
    res = client.get(
        f'{LINKS_MAIN_ROUTE}?page=1&page_size=100000',
        headers=headers
    )
    assert res.status_code == 400


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
        f'{LINKS_BY_CATEGORY_ROUTE}/{NEW_CREATED_CATEGORY_ID+100}',
        headers=headers
    )
    assert res.status_code == 404


def test_update_categories_of_a_link_accepted(client):
    """curl -i -H "Content-Type: application/json"
    -H "Authorization: Bearer $x" -X PUT
    -d '{"new_categories": ["test_1", "test_3"]}'
    localhost:5000/links/2/category
    """
    address = LINKS_UPDATE_CATEGORY.replace(
        '<int:id>', str(NEW_CREATED_LINK_ID)
    )

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {
        "new_categories": NEW_CATEGORIES
    }

    res = client.put(
        address,
        headers=headers,
        data=json.dumps(data)
    )
    assert res.status_code == 200


def test_validate_new_categories_are_replaced_accepted(client):
    """ Check if categories are updated in DB or not"""
    headers = {
        'Authorization': f"Bearer {TOKEN}"
    }
    res = client.get(
        f'{LINKS_MAIN_ROUTE}/{NEW_CREATED_LINK_ID}',
        headers=headers
    )

    updated_categories = json.loads(
        res.get_data(as_text=True))[0]["categories"]

    for category in updated_categories:
        assert(category['name'] in NEW_CATEGORIES)


def test_update_categories_of_a_link_delete_all_categories_accepted(client):
    address = LINKS_UPDATE_CATEGORY.replace(
        '<int:id>', str(NEW_CREATED_LINK_ID)
    )

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {}

    res = client.put(
        address,
        headers=headers,
        data=json.dumps(data)
    )
    assert res.status_code == 200


def test_update_user_publicity_to_true_accepted(client):
    """Change users publicity to true, to pass the next test
    if there is no other public user in DB
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }
    data = {
        'publicity': True
    }
    res = client.put(
        USER_PUBLICITY_ROUTE,
        data=json.dumps(data),
        headers=headers
    )
    assert res.status_code == 200


def test_get_user_activity_with_date_accepted(client):
    """curl -i -H "Content-Type: application/json" -H "Authorization: Bearer $x"
    -X POST -d '{"date_from": "2020-12-1 16:09"}' localhost:5000/user/activity
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {"date_from": VALID_DATE}

    res = client.post(
        USER_ACTIVITY_ROUTE,
        headers=headers,
        data=json.dumps(data)
    )

    global NEW_CREATED_USER_ID
    NEW_CREATED_USER_ID = json.loads(
        res.get_data(as_text=True))[0]['user_id']
    assert res.status_code == 200


def test_get_user_activities_paginated_without_date_accepted(client):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {}
    res = client.post(
        f'{USER_ACTIVITY_ROUTE}?page=1&page_size=1',
        headers=headers,
        data=json.dumps(data)
    )
    assert res.status_code == 200


def test_get_user_activities_paginated_with_date_accepted(client):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {"date_from": VALID_DATE}
    res = client.post(
        f'{USER_ACTIVITY_ROUTE}?page=1&page_size=1',
        headers=headers,
        data=json.dumps(data)
    )
    assert res.status_code == 200


def test_get_user_activities_paginated_not_found_rejected(client):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {"date_from": VALID_DATE}
    res = client.post(
        f'{USER_ACTIVITY_ROUTE}?page=1000&page_size=1',
        headers=headers,
        data=json.dumps(data)
    )
    assert res.status_code == 404


def test_get_user_activities_paginated_exceed_limit_rejected(client):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {"date_from": VALID_DATE}
    res = client.post(
        f'{USER_ACTIVITY_ROUTE}?page=1&page_size=100000',
        headers=headers,
        data=json.dumps(data)
    )
    assert res.status_code == 400


def test_get_user_activities_paginated_invalid_date_rejected(client):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {"date_from": "2020-14-7 16:09"}
    res = client.post(
        f'{USER_ACTIVITY_ROUTE}?page=1&page_size=100000',
        headers=headers,
        data=json.dumps(data)
    )
    assert res.status_code == 400


def test_get_user_activity_without_date_accepted(client):
    """curl -i -H "Content-Type: application/json" -H "Authorization: Bearer $x"
    -X POST -d '{}' localhost:5000/user/activity
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {}

    res = client.post(
        USER_ACTIVITY_ROUTE,
        headers=headers,
        data=json.dumps(data)
    )

    assert res.status_code == 200


def test_get_user_activity_invalid_date_failed(client):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {"date_from": "20-12-1 16:09"}

    res = client.post(
        USER_ACTIVITY_ROUTE,
        headers=headers,
        data=json.dumps(data)
    )
    assert res.status_code == 400


def test_get_user_activity_not_found_failed(client):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {"date_from": "2025-12-1 15:00"}

    res = client.post(
        USER_ACTIVITY_ROUTE,
        headers=headers,
        data=json.dumps(data)
    )
    assert res.status_code == 404


def test_get_public_user_links_accepted(client):
    """curl -i -H "Content-Type: application/json" -H "Authorization: Bearer $x"
    -X POST -d '{}' localhost:5000/user/1/links
    """
    address = LINKS_BY_USER_ID.replace(
        '<int:id>', str(NEW_CREATED_USER_ID)
    )
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {}

    res = client.post(
        address,
        headers=headers,
        data=json.dumps(data)
    )
    assert res.status_code == 200


def test_get_public_user_links_with_date_accepted(client):
    """curl -i -H "Content-Type: application/json" -H "Authorization: Bearer $x"
    -X POST -d '{"date_from": "2020-12-1 15:00"}' localhost:5000/user/1/links
    """
    address = LINKS_BY_USER_ID.replace(
        '<int:id>', str(NEW_CREATED_USER_ID)
    )
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {"date_from": VALID_DATE}

    res = client.post(
        address,
        headers=headers,
        data=json.dumps(data)
    )
    assert res.status_code == 200


def test_get_public_user_links_user_not_found_rejected(client):
    address = LINKS_BY_USER_ID.replace(
        '<int:id>', str(NEW_CREATED_USER_ID+1000)
    )
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {"date_from": VALID_DATE}

    res = client.post(
        address,
        headers=headers,
        data=json.dumps(data)
    )
    assert res.status_code == 404


def test_get_public_user_links_wrong_date_rejected(client):
    address = LINKS_BY_USER_ID.replace(
        '<int:id>', str(NEW_CREATED_USER_ID)
    )
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {"date_from": "2020-120-1 15:00"}

    res = client.post(
        address,
        headers=headers,
        data=json.dumps(data)
    )
    assert res.status_code == 400


def test_get_public_user_links_no_link_found_rejected(client):
    address = LINKS_BY_USER_ID.replace(
        '<int:id>', str(NEW_CREATED_USER_ID)
    )
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {"date_from": "2025-12-1 15:00"}

    res = client.post(
        address,
        headers=headers,
        data=json.dumps(data)
    )
    assert res.status_code == 404


def test_get_public_user_links_paginated_accepted(client):
    address = LINKS_BY_USER_ID.replace(
        '<int:id>', str(NEW_CREATED_USER_ID)
    )
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {}

    res = client.post(
        f'{address}?page=1&page_size=1',
        headers=headers,
        data=json.dumps(data)
    )
    assert res.status_code == 200


def test_get_public_user_links_paginated_with_date_accepted(client):
    address = LINKS_BY_USER_ID.replace(
        '<int:id>', str(NEW_CREATED_USER_ID)
    )
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {"date_from": VALID_DATE}

    res = client.post(
        f'{address}?page=1&page_size=1',
        headers=headers,
        data=json.dumps(data)
    )
    assert res.status_code == 200


def test_get_public_user_links_paginated_not_found_rejected(client):
    address = LINKS_BY_USER_ID.replace(
        '<int:id>', str(NEW_CREATED_USER_ID)
    )
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {"date_from": VALID_DATE}

    res = client.post(
        f'{address}?page=10000&page_size=1',
        headers=headers,
        data=json.dumps(data)
    )
    assert res.status_code == 404


def test_get_public_user_links_paginated_exceed_limit_rejected(client):
    address = LINKS_BY_USER_ID.replace(
        '<int:id>', str(NEW_CREATED_USER_ID)
    )
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {"date_from": VALID_DATE}

    res = client.post(
        f'{address}?page=1&page_size=10000',
        headers=headers,
        data=json.dumps(data)
    )
    assert res.status_code == 400


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


def test_update_categories_of_a_link_rejected(client):
    """
    THIS LINK ID IS DELETED BECAUSE OF PREVIOUS CALL
    """

    address = LINKS_UPDATE_CATEGORY.replace(
        '<int:id>', str(NEW_CREATED_LINK_ID)
    )

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {TOKEN}"
    }
    data = {
        "new_categories": ["SOME_THING_NOT_IMPORTANT"]
    }

    res = client.put(
        address,
        headers=headers,
        data=json.dumps(data)
    )
    assert res.status_code == 404
