from flask import session

from todo_app.data.Item import Item
import requests, os

TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY')
TRELLO_TOKEN = os.environ.get('TRELLO_TOKEN')
TRELLO_BOARD_ID = "608c0972ee945e2cd7fb1211"
TRELLO_BOARD_TODO_LIST_ID = "608c0972ee945e2cd7fb1212"
TRELLO_BOARD_DONE_LIST_ID = "608c0972ee945e2cd7fb1214"


def _url(path):
    return 'https://api.trello.com/1/' + path

def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of todo items.
    """
    query = {
    'key': TRELLO_API_KEY,
    'token': TRELLO_TOKEN
    }
    response = requests.get(_url(f'boards/{TRELLO_BOARD_ID}/cards'), params=query).json()

    items = []

    for card in response:
        status = "Completed" if card['dueComplete'] == True else "Not Started"
        
        item = Item(id=card['id'], title=card['name'], status=status)

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
    query = {
    'key': TRELLO_API_KEY,
    'token': TRELLO_TOKEN
    }
    response = requests.get(_url(f'cards/{id}'), params=query).json()
    item = { 'id': response['id'], 'title': response['name'], 'status': status }
    return item



def add_item(title):
    """
    Adds a new item with the specified title.

    Args:
        title: The title of the item.

    """

    query = {
    'key': TRELLO_API_KEY,
    'token': TRELLO_TOKEN,
    'idList': TRELLO_BOARD_TODO_LIST_ID,
    'name': title
    }
    
    response = requests.post(_url('cards'), params=query).json()


def complete_item(id):
    """
    Updates an existing item to Complete in the Trell board.

    Args:
        item: The item to save.
    """
    query = {
    'key': TRELLO_API_KEY,
    'token': TRELLO_TOKEN,
    'idList': TRELLO_BOARD_DONE_LIST_ID,
    'dueComplete': 'true'
    }
    requests.put(_url(f'cards/{id}'), params=query)

def delete_item(id):
    """
    Delets an existing item in the Trello board.

    Args:
        item: The item to delete.
    """

    query = {
    'key': TRELLO_API_KEY,
    'token': TRELLO_TOKEN
    }
    
    response = requests.delete(_url(f'cards/{id}'), params=query).json()