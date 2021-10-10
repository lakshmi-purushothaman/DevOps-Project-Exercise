from flask import session

from todo_app.data.Item import Item
import requests, os



class TodoService:
    def __init__(self):
        self.board_id = None
        self.todo_list_id = None
        self.done_list_id = None
        self.doing_list_id = None
        self.TRELLO_API_KEY = os.environ.get('TRELLO_API_KEY')
        self.TRELLO_TOKEN = os.environ.get('TRELLO_TOKEN')
        self.TRELLO_BOARD_NAME = os.environ.get('TRELLO_BOARD_NAME')
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
            'key': self.TRELLO_API_KEY,
            'token': self.TRELLO_TOKEN,
            'name': self.TRELLO_BOARD_NAME
        }
        response = requests.post(self._url('boards'), params=query).json()
        self.board_id = response['id']
        return self.board_id
    
    def members_board_lookup(self):
        """
        Looksup for all the boards associated with members

        If default board name exists set the id to board id.
        """
        query = {
        'key': self.TRELLO_API_KEY,
        'token': self.TRELLO_TOKEN
        }
        
        response = requests.get(self._url(f'members/me/boards'), params=query).json()

        for boards in response:
            if boards['name'] == self.TRELLO_BOARD_NAME and boards['closed'] == False:
                self.board_id = boards['id']
    
    def setup_board_lists(self):
        """
        Looks up for a lists in the board and sets Todo and Done list id's to the default board id lists

        """
        query = {
        'key': self.TRELLO_API_KEY,
        'token': self.TRELLO_TOKEN
        }
        response = requests.get(self._url(f'boards/{self.board_id}/lists'), params=query).json()
        for list in response:
            if list['name'] == "To Do":
                self.todo_list_id = list['id']
            elif list['name'] == "Done":
                self.done_list_id = list['id']
            elif list['name'] == "Doing":
                self.doing_list_id = list['id']

    def delete_board(self, board_id):
        query = {
            'key': self.TRELLO_API_KEY,
            'token': self.TRELLO_TOKEN,
            'name': self.TRELLO_BOARD_NAME
        }
        response = requests.delete(self._url(f'boards/{board_id}'), params=query).json()
        return response

    def archive_cards(self):
        board_list=[self.todo_list_id, self.doing_list_id, self.done_list_id]

        query = {
            'key': self.TRELLO_API_KEY,
            'token': self.TRELLO_TOKEN,
            'name': self.TRELLO_BOARD_NAME
        }
        for list_id in board_list:
            response = requests.post(self._url(f'/lists/{list_id}/archiveAllCards'), params=query).json()
        return response

    def get_items(self):
        """
        Fetches all saved items from the session.

        Returns:
            list: The list of todo items.
        """
        query = {
        'key': self.TRELLO_API_KEY,
        'token': self.TRELLO_TOKEN
        }
        response = requests.get(self._url(f'boards/{self.board_id}/cards'), params=query).json()
        
        status_dict = {
            self.todo_list_id : 'Todo',
            self.doing_list_id : 'Doing',
            self.done_list_id : 'Done'
        }

        items = []

        for card in response:
            card_idlist = card['idList']

            status = status_dict[card_idlist]
            
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
        'key': self.TRELLO_API_KEY,
        'token': self.TRELLO_TOKEN,
        'idList': self.todo_list_id,
        'name': title
        }
        print(self.todo_list_id)
        response = requests.post(self._url('cards'), params=query).json()


    def move_to_done(self, id):
        """
        Updates an existing item to Done in the Trell board.

        Args:
            item: The item to save.
        """
        query = {
        'key': self.TRELLO_API_KEY,
        'token': self.TRELLO_TOKEN,
        'idList': self.done_list_id,
        'dueComplete': 'true'
        }
        requests.put(self._url(f'cards/{id}'), params=query)

    def move_to_doing(self, id):
        """
        Updates an existing item to Doing in the Trell board.

        Args:
            item: The item to save.
        """
        query = {
        'key': self.TRELLO_API_KEY,
        'token': self.TRELLO_TOKEN,
        'idList': self.doing_list_id,
        'dueComplete': 'false'
        }
        requests.put(self._url(f'cards/{id}'), params=query)

    def move_to_todo(self, id):
        """
        Updates an existing item to Todo in the Trell board.

        Args:
            item: The item to save.
        """
        query = {
        'key': self.TRELLO_API_KEY,
        'token': self.TRELLO_TOKEN,
        'idList': self.todo_list_id,
        'dueComplete': 'false'
        }
        requests.put(self._url(f'cards/{id}'), params=query)

    def delete_item(self, id):
        """
        Delets an existing item in the Trello board.

        Args:
            item: The item to delete.
        """

        query = {
        'key': self.TRELLO_API_KEY,
        'token': self.TRELLO_TOKEN
        }
        
        response = requests.delete(self._url(f'cards/{id}'), params=query).json()