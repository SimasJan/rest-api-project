import requests
import json

URL = 'http://127.0.0.1:5000'

def failed_test_formatter(msg, expected, received):
    """Utility function to format failed test outputs."""
    print(f"{msg} | Expected: `{expected}` | Received: `{received}`")


# testing nothing should work without authorization header
def test_get_all_items_no_authorization_should_fail():
    rsp = requests.get(URL+"/item").json()
    assert rsp['error'] == 'authorization_required', failed_test_formatter(
        f'{__name__}, failed',
        'authorization_required',
        rsp
    )

def test_update_item_with_no_authorization_should_fail():
    rsp = requests.put(URL + '/item/1').json()
    assert rsp['error'] == 'authorization_required', failed_test_formatter(
        f'{__name__}, failed!',
        'authorization_required',
        rsp
    )

def test_create_item_with_no_authorization_should_fail():
    rsp = requests.post(URL + '/item').json()
    assert rsp['error'] == 'authorization_required', failed_test_formatter(
        f'{__name__}, failed!',
        'authorization_required',
        rsp
    )

# testing items api (with authorization)

def test_get_all_items():
    ""
    pass

def test_create_item():
    pass

def test_get_item():
    pass

def test_update_item():
    pass

