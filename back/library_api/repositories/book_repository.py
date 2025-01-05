from library_project.settings import *
from bson.objectid import ObjectId
class BookRepository:
    def __init__(self):
        """
        Initialize a new BookRepository instance.
        Sets up the database client, database, and collection for books.
        """
        self.client = client
        self.db = db
        self.collection = self.db['livres']

    def create_book(self, book_data):
        """
        Create a new book entry in the database.

        Args:
            book_data (dict): A dictionary containing book information.

        Returns:
            bool: True if the book was successfully created, False otherwise.
        """
        result = self.collection.insert_one(book_data)
        return result.acknowledged

    def get_book(self, _id):
        """
        Retrieve a book entry from the database by its ID.

      result = self.collection.update_one({'_id': ObjectId(_id)}, {'$set': update_data})
      return result

        Returns:
            dict: The book data if found, None otherwise.
        """
        book_data = self.collection.find_one({'_id': ObjectId(_id)})
        return book_data

    def get_books(self):
        """
        Retrieve all book entries from the database.

        Returns:
            pymongo.cursor.Cursor: A cursor to the book documents.
        """
        book_data = self.collection.find()
        return book_data

    def update_book(self, book_id, update_data):
        try:
            object_id = ObjectId(book_id)
            # Utilisez $set pour mettre à jour uniquement les champs spécifiés
            result = self.collection.update_one(
                {"_id": object_id},
                {"$set": update_data}
            )
            print(f"Mise à jour effectuée - modified_count: {result.modified_count}")
            return result
        except Exception as e:
            print(f"Erreur lors de la mise à jour: {str(e)}")
            raise

    def delete_book(self, _id):
        """
        Delete a book entry from the database.

        Args:
            _id (str): The ID of the book to delete.

        Returns:
            pymongo.results.DeleteResult: The result of the delete operation.
        """
        result = self.collection.delete_one({'_id': ObjectId(_id)})
        return result