from library_project.settings import *
from bson.objectid import ObjectId
class BookRepository:
 def __init__(self):

   self.client = client
   self.db = db
   self.collection = self.db['biblio']

 def create_book(self, book_data):

   result = self.collection.insert_one(book_data)
   return result.acknowledged

 def get_book(self, _id):

   book_data = self.collection.find_one({'_id': ObjectId(_id)})
   return book_data

 def get_books(self):

    book_data = self.collection.find()
    return book_data

 def update_book(self, _id, update_data):

      result = self.collection.update_one({'_id': ObjectId(_id)}, {'$set': update_data})
      return result

 def delete_book(self, _id):

    result = self.collection.delete_one({'_id': ObjectId(_id)})
    return result

