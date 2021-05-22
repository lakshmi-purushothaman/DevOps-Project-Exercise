from flask import session

from todo_app.data.Item import Item
import requests, os

TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY')
TRELLO_TOKEN = os.environ.get('TRELLO_TOKEN')
TRELLO_BOARD_NAME = "Devops Course Project Board"

class TodoService:
    def __init__(self):
        self.board_id = None
        self.todo_list_id = None
        self.done_list_id = None
        self.setup_board()

    def _url(self, path):
        return 'https://api.trello.com/1/' + path

    def setup_board(self):
        self.members_board_lookup()
        if self.board_id == None:
            self.create_board()
        self.setup_board_lists()

    def create_board(self):
        query = {
            'key': TRELLO_API_KEY,
            'token': TRELLO_TOKEN,
            'name': TRELLO_BOARD_NAME
        }
        response = requests.post(self._url('boards'), params=query).json()
        self.board_id = response['id']
    
    def members_board_lookup(self):
        """
        Looksup for all the boards associated with members

        If default board name exists set the id to board id.
        """
        query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN
        }
        response = requests.get(self._url(f'members/me/boards'), params=query).json()

        for boards in response:
            if boards['name'] == TRELLO_BOARD_NAME and boards['closed'] == False:
                self.board_id = boards['id']
    
    def setup_board_lists(self):
        """
        Looks up for a lists in the board and sets Todo and Done list id's to the default board id lists

        """
        query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN
        }
        response = requests.get(self._url(f'boards/{self.board_id}/lists'), params=query).json()
        for list in response:
            if list['name'] == "To Do":
                self.todo_list_id = list['id']
            elif list['name'] == "Done":
                self.done_list_id = list['id']

    def get_items(self):
        """
        Fetches all saved items from the session.

        Returns:
            list: The list of todo items.
        """
        query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN
        }
        response = requests.get(self._url(f'boards/{self.board_id}/cards'), params=query).json()

        items = []

        for card in response:
            status = "Completed" if card['dueComplete'] == True else "Not Started"
            
            item = Item(id=card['id'], title=card['name'], status=status)

            items.append(item)
        return items


    def add_item(self, title):
        """
        Adds a new item with the specified title.

        Args:
            title: The title of the item.

        """

        query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN,
        'idList': self.todo_list_id,
        'name': title
        }
        print(self.todo_list_id)
        response = requests.post(self._url('cards'), params=query).json()


    def complete_item(self, id):
        """
        Updates an existing item to Complete in the Trell board.

        Args:
            item: The item to save.
        """
        query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN,
        'idList': self.done_list_id,
        'dueComplete': 'true'
        }
        requests.put(self._url(f'cards/{id}'), params=query)

    def delete_item(self, id):
        """
        Delets an existing item in the Trello board.

        Args:
            item: The item to delete.
        """

        query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN
        }
        
        response = requests.delete(self._url(f'cards/{id}'), params=query).json()