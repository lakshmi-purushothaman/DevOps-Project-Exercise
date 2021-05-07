from flask import session

import requests
_DEFAULT_ITEMS = [
    { 'id': 1, 'status': 'Not Started', 'title': 'List saved todo items' },
    { 'id': 2, 'status': 'Not Started', 'title': 'Allow new items to be added' }
]

def _url(path):
    return 'https://api.trello.com/' + path

def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of todo items.
    """
    query = {
    'key': 'f0d5da5df98284c240a5a8a65a0b0e96',
    'token': '546b3a441384d0d83b195b85d8e58c9643542c3974a20100284bfe639db057ad'
    }
    response = requests.get(_url('1/boards/608c0972ee945e2cd7fb1211/cards'), params=query).json()

    items = []

    for card in response:
        status = "Completed" if card['dueComplete'] ==True else "Not Started"
        item = { 'id': card['id'], 'title': card['name'], 'status': status }
        items.append(item)
    return items

def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == int(id)), None)


def add_item(title):
    """
    Adds a new item with the specified title.

    Args:
        title: The title of the item.

    """

    query = {
    'key': 'f0d5da5df98284c240a5a8a65a0b0e96',
    'token': '546b3a441384d0d83b195b85d8e58c9643542c3974a20100284bfe639db057ad',
    'idList': '608c0972ee945e2cd7fb1212',
    'name': title
    }
    
    response = requests.post(_url('1/cards'), params=query).json()


def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    existing_items = get_items()
    updated_items = [item if item['id'] == existing_item['id'] else existing_item for existing_item in existing_items]

    session['items'] = updated_items

    return item

def delete_item(item):
    """
    Delets an existing item in the session. If no existing item matches the ID of the specified item, nothing is deleted.

    Args:
        item: The item to delete.
    """
    existing_items = get_items()
    try:
        existing_items.remove(item)
        session['items'] = existing_items
    except ValueError:
        print('Item doesnot exist')