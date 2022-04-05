from flask_login import UserMixin, AnonymousUserMixin

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        if id == 80856928:
            self.role = "writer"
        else:
            self.role = "reader"

    def get_id(self):
        return self.id

class MyAnonymousUser(AnonymousUserMixin):
    def __init__(self):
        self.role = "writer"
