class ViewModel:
    def __init__(self, items, user_role):
        self._items = items
        self._user_role = user_role
    
    @property
    def items(self):
        return self._items
    
    @property
    def todo_items(self):
        return [item for item in self._items if item.status == 'Todo']

    
    @property
    def done_items(self):
        return [item for item in self._items if item.status == 'Done']
        

    @property
    def doing_items(self):
        return [item for item in self._items if item.status == 'Doing']

    @property
    def user_role(self):
        return self._user_role
