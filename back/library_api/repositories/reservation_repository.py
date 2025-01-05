from library_project.settings import *
from bson.objectid import ObjectId
from datetime import datetime,timedelta

class ReservationRepository:
    def __init__(self):
        """
        Initialise une instance de Repository pour gérer les réservations.
        """
        self.client = client
        self.db = db
        self.collection = self.db['reservations']

    def calculate_end_date(self, duration_str):
        """
        Calcule la date de fin en fonction de la durée sous forme de chaîne.
        
        Args:
            duration_str (str): La durée de la réservation sous forme de chaîne (ex: "2 hours", "3 days").
        
        Returns:
            datetime: La date de fin calculée.
        """
        duration_parts = duration_str.split()
        if len(duration_parts) == 2:
            value = int(duration_parts[0])
            unit = duration_parts[1].lower()
            if unit in ['hour', 'hours']:
                return datetime.now() + timedelta(hours=value)
            elif unit in ['day', 'days']:
                return datetime.now() + timedelta(days=value)
        return datetime.now()  # Retourne l'heure actuelle si la durée est invalide

    def create_reservation(self, book_id, student_id, duration):
        """
        Crée une nouvelle réservation dans la base de données.
        
        Args:
            book_id (str): L'ID du livre réservé.
            student_id (str): L'ID de l'étudiant qui fait la réservation.
            duration (str): La durée de la réservation sous forme de chaîne (ex: "2 hours", "1 day").
        
        Returns:
            bool: True si la réservation a été créée avec succès, False sinon.
        """
        # Calculer la date de fin de réservation
        date_fin_reservation = self.calculate_end_date(duration)

        reservation_data = {
            'book': ObjectId(book_id),
            'student': ObjectId(student_id),
            'status': 'En cours',  # Par défaut, la réservation est en attente.
            'date_reservation': datetime.now(),
            'duration': duration,
            'date_fin_reservation': date_fin_reservation
        }
        result = self.collection.insert_one(reservation_data)
        return result.acknowledged

    def get_reservation(self, reservation_id):
        """
        Récupère une réservation par son ID.

        Args:
            reservation_id (str): L'ID de la réservation à récupérer.

        Returns:
            dict: La réservation si elle existe, sinon None.
        """
        reservation_data = self.collection.find_one({'_id': ObjectId(reservation_id)})
        return reservation_data

    def get_reservations(self):
        """
        Récupère toutes les réservations.

        Returns:
            pymongo.cursor.Cursor: Un curseur sur les documents des réservations.
        """
        reservation_data=self.collection.find()
        return reservation_data

    def update_reservation(self, reservation_id, update_data):
        """
        Met à jour une réservation dans la base de données.

        Args:
            reservation_id (str): L'ID de la réservation à mettre à jour.
            update_data (dict): Les données à mettre à jour.

        Returns:
            pymongo.results.UpdateResult: Le résultat de l'opération de mise à jour.
        """
        result = self.collection.update_one({'_id': ObjectId(reservation_id)}, {'$set': update_data})
        return result

    def delete_reservation(self, reservation_id):
        """
        Supprime une réservation de la base de données.

        Args:
            reservation_id (str): L'ID de la réservation à supprimer.

        Returns:
            pymongo.results.DeleteResult: Le résultat de l'opération de suppression.
        """
        result = self.collection.delete_one({'_id': ObjectId(reservation_id)})
        return result
