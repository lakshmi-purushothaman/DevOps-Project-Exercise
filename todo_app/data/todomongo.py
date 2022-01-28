from bson.objectid import ObjectId
import pymongo
import os

from todo_app.data.Item import Item


class TodoMongoAccessService:
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
        self.db = self.client[os.getenv("DBNAME")]
        self.collection =self.db[os.getenv("COLLECTIONAME")]
        

    def get_items(self):
        """
        Fetches all saved items from the items collection.

        Returns:
            list: The list of todo items.
        """
        cards = self.collection.find()
     
        items = []

        for card in cards:
            
            item = Item(id=card['_id'], title=card['name'], status=card['status'])

            items.append(item)
        return items

    def add_item(self, title, status):
        """
        Adds a new item with the specified title.

        Args:
            title: The title of the item.

        """
        card = {"name":title, "status": status}
        self.collection.insert_one(card)
    
    def update_todo_item_status(self, id, status):
        """
        Updates an existing item in the Items Collection.

        Args:
            item: The item to save.
        """
        self.collection.update_one({"_id":ObjectId(id)}, {"$set":{"status": status}})

    def delete_item(self, id):
        """
        Deletes an existing item in the Items collection.

        Args:
            item: The item to delete.
        """
        self.collection.delete_one({"_id":ObjectId(id)})