class BookSerializer:
    @staticmethod
    def serialize(book_data):
        """
        Serialize book data into a format suitable for API responses.

        Args:
            book_data (dict): A dictionary containing book data.

        Returns:
            dict: A serialized version of the book data.
        """
        
        serialized_book = {
            'id': str(book_data['_id']),  # Convert ObjectId to string
            'N': book_data.get('N', ''),
            'BIBID': book_data.get('BIBID', ''),
            'ITEMID': book_data.get('ITEMID', ''),
            'Code_barre': book_data.get('Code_barre', ''),
            'D_CREATION': book_data.get('CREATION', ''),
            'D_MODIF': book_data.get('MODIF', ''),
            'Cote': book_data.get('Cote', ''),
            'Inventaire': book_data.get('Inventaire', ''),
            'epn': book_data.get('epn', ''),
            'Titre': book_data.get('Titre', ''),
            'Auteur': book_data.get('Auteur', ''),
            'Locale': book_data.get('Locale', ''),
            'Staff_Note': book_data.get('Staff_Note', ''),
            'Public_Note': book_data.get('Public_Note', ''),
            'ISBN_A': book_data.get('ISBN_A', ''),
            'ISBN_Z': book_data.get('ISBN_Z', ''),
            'Item_class': book_data.get('Item_class', ''),
            'Specialite': book_data.get('Specialite', ''),
            'Nb_Page': book_data.get('Nb_Page', ''),
            'Date_edition': book_data.get('Date_edition', ''),
            'Editeur': book_data.get('Editeur', ''),
            'Prix': book_data.get('Prix', ''),
            'Etas':book_data.get('Etas', '')
        }
        return serialized_book