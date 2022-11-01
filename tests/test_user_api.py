from email import header
import requests
import json

URL = 'http://127.0.0.1:5000'
# user_payload = {'username': 'test_user1', 'password': 'user_test1'}

def failed_test_formatter(msg, expected, received):
    """Utility function to format failed test outputs."""
    print(f"{msg} | Expected: `{expected}` | Received: `{received}`")


def test_register_user(endpoint='/register'):
    test_payload = {'username': 'test_user1', 'password': 'user_test1'}
    rsp = requests.post(URL + endpoint, json=test_payload).json()
    assert rsp['message'] == 'User created successfully.', failed_test_formatter(
        'test_register_user() failed!', 
        'User created successfully.', 
        rsp['message']
    )

def test_login_user(endpoint='/login'):
    test_payload = {'username': 'test_user1', 'password': 'user_test1'}
    rsp = requests.post(URL + endpoint, json=test_payload).json()
    assert 'access_token' in rsp, failed_test_formatter(
        'test_login_user() failed!',
        'access_token key',
        rsp['message']
    )

def test_get_user(endpoint='/user/', user_id=1):
    rsp = requests.get("{}{}{}".format(URL, endpoint, user_id)).json()
    assert rsp['id'] == user_id, failed_test_formatter(
        "test_get_user() failed!",
        'rsp.id == user_id',
        rsp
    )

def test_logout_user(endpoint='/logout'):
    test_payload = {'username': 'test_user1', 'password': 'user_test1'}
    # login to get access token, reuse it in headers to log out
    rsp = requests.post(URL + "/login", json=test_payload).json()
    token = rsp['access_token']
    rsp = requests.post(URL + endpoint, 
        headers={'Authorization': f'Bearer {token}'},
        json=test_payload
    ).json()

    assert rsp['message'] == "Successfully logged out.", failed_test_formatter(
        'test_logout_user() failed!',
        'Successfully logged out.',
        rsp['message']
    )

def test_delete_user(endpoint='/user/', user_id=2):
    """
        1. Get access token for the `test_user1` (required to delete the user created in step 1).
        2. Create a new user (this should be a user with ID = 2)
        3. Delete the new user.
    """
    admin_user_payload = {'username': 'test_user1', 'password': 'user_test1'}
    test_payload = {'username': 'delete_user', 'password': 'delete_user'}

    token = requests.post(
        "{}/login".format(URL), 
        json=admin_user_payload
    ).json()['access_token']
    
    rsp = requests.post(
        "{}/register".format(URL), 
        json=test_payload
    ).json()
    
    rsp = requests.delete(
        "{}{}{}".format(URL, endpoint, user_id), 
        headers={'Authorization': f'Bearer {token}'},
        json=test_payload
    ).json()
    
    assert rsp['message'] == 'User deleted.', failed_test_formatter(
        'test_delete_user() failed!',
        'User deleted.',
        rsp
    )