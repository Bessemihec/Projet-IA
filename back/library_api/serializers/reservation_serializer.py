class ReservationSerializer:
    @staticmethod
    def serialize(reservation):
        """
        Sérialise une réservation pour l'envoyer comme réponse JSON.
        
        Retourne :
        - Un dictionnaire représentant la réservation
        """
        return {
            'id': str(reservation['_id']),  # Conversion de l'ObjectId en string
            'book_id': str(reservation['book']),  # Id du livre
            'student_id': str(reservation['student']),  # Id de l'étudiant
            'status': reservation['status'],  # Statut de la réservation
            'date_reservation': reservation['date_reservation'].isoformat(),  # Date sous format ISO 8601
            'duration': reservation['duration'],  # Durée de la réservation en tant que chaîne
            'date_fin_reservation': reservation['date_fin_reservation'].isoformat()  # Date de fin sous format ISO 8601
        }
