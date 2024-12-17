from bson import ObjectId
from library_project.settings import client, db

class BookshelfRepository:
    def __init__(self):

        """
        Initialize a new BookshelfRepository instance.
        Sets up the database client, database, and collection for bookshelves.
        """

        self.client = client
        self.db = db
        self.collection = self.db['bookshelves']
        
    def add_book_to_shelf(self, book_id, user_id):

        """
        Add a book to the user's bookshelf.

        Args:
            book_id (str): The ID of the book to add.
            user_id (str): The ID of the user whose shelf to add the book to.

        Returns:
            bool: True if the book was successfully added to the shelf, False otherwise.
        """

        shelf_data = {
            'book_id': ObjectId(book_id),
            'user_id': ObjectId(user_id),
        }
        result = self.collection.insert_one(shelf_data)
        return result.acknowledged

    def get_shelf(self, user_id):

        """
        Get the book IDs from the user's bookshelf.

        Args:
            user_id (str): The ID of the user whose shelf to retrieve.

        Returns:
            list: A list of book IDs in the user's shelf.
        """

        shelves = self.collection.find({'user_id': ObjectId(user_id)})
        book_ids = [str(shelf['book_id']) for shelf in shelves]
        return book_ids

    
    def remove_book_to_shelf(self, user_id, book_id):

        """
        Remove a book from the user's bookshelf.

        Args:
            user_id (str): The ID of the user whose shelf to remove the book from.
            book_id (str): The ID of the book to remove from the shelf.

        Returns:
            bool: True if the book was successfully removed from the shelf, False otherwise.
        """
        
        result = self.collection.delete_one({'user_id': ObjectId(user_id), 'book_id': ObjectId(book_id)})
        return result.deleted_count > 0