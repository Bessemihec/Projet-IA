import qrcode
from datetime import datetime, timedelta

class User:
    def __init__(self, email, username, password, role,qr_code=None):
        """
        Initialise une instance utilisateur.

        Args:
            email (str): L'email de l'utilisateur.
            username (str): Le nom d'utilisateur.
            password (str): Le mot de passe.
            role (str): Le rôle de l'utilisateur ('étudiant', 'bibliothécaire', 'admin').
        """
        self.email = email
        self.username = username
        self.password = password
        self.role = role
        self.qr_code = qr_code 

    def __str__(self):
        """
        Retourne une représentation sous forme de chaîne de l'utilisateur.

        Returns:
            str: Le nom d'utilisateur.
        """
        return f"{self.username} ({self.role})"

class Student(User):
    def __init__(self, email, username, password, university, speciality):
        """
        Initialise une instance étudiant.

        Args:
            email (str): L'email de l'étudiant.
            username (str): Le nom d'utilisateur de l'étudiant.
            password (str): Le mot de passe.
            university (str): L'université de l'étudiant.
            speciality (str): La spécialité de l'étudiant.
        """
        super().__init__(email, username, password, "étudiant")
        self.university = university
        self.speciality = speciality

class Librarian(User):
    def __init__(self, email, username, password):
        """
        Initialise une instance bibliothécaire.

        Args:
            email (str): L'email du bibliothécaire.
            username (str): Le nom d'utilisateur.
            password (str): Le mot de passe.
        """
        super().__init__(email, username, password, "bibliothécaire")

    def __str__(self):
        return f"{self.username} (Bibliothécaire)"

class Admin(User):
    def __init__(self, email, username, password):
        """
        Initialise une instance administrateur.

        Args:
            email (str): L'email de l'administrateur.
            username (str): Le nom d'utilisateur.
            password (str): Le mot de passe.
        """
        super().__init__(email, username, password, "admin")

    def __str__(self):
        return f"{self.username} (Admin)"