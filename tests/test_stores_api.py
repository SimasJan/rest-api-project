import requests
import json

URL = 'http://127.0.0.1:5000'

def test_get_stores():
    rsp = requests.get(URL+'/store').json()
    assert rsp == {}, "test_get_stores() failed!"

def test_create_store():
    test_name = 'test_store'
    rsp = requests.post(URL+'/store', json={'name': test_name}).json()
    assert rsp['name'] == test_name

def test_create_item():
    test_item = {
        "name": "Chair",
        "price": 18.99,
        "store_id": "3890e5e190a645d6b34209469a00ff58"
    }
    rsp = requests.post(URL + '/item', json=json.dumps(test_item)).json()
    print(rsp)

# def test_add_item_to_store():
#     test_item = {'name': 'test_item', 'price': 0.00}
#     rsp = requests.post(URL+'/store/test_store/item', json=test_item).json()
#     assert rsp == test_item

# def test_get_store_by_name():
#     test_store_name = 'test_store'
#     rsp = requests.get(URL+'/store/'+test_store_name).json()
#     assert rsp['name'] == test_store_name

# def test_get_item_in_store():
#     test_store_name = 'test_store'
#     test_store_items = {'name': 'test_item', 'price': 0.00}
#     rsp = requests.get(URL + '/store/' + test_store_name + '/item').json()
#     # in case there are more than 1 item, fetch only first one.
#     items = rsp['items'] if len(rsp['items']) == 1 else rsp['items'][0]
#     assert items == test_store_items
