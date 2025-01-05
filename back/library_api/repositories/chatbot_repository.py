from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Connexion à MongoDB
mongo_client = MongoClient(os.getenv("MONGO_DB_URI"))
db = mongo_client[os.getenv("MONGO_DB_NAME")]
collection = db["livres"]  

class chatbot_repository:
    """
    Classe pour gérer les interactions avec MongoDB.
    """

    @staticmethod
    def fetch_books_by_keywords(keywords, limit=10):
        """
        Récupère les livres en fonction des mots-clés.
        :param keywords: Dictionnaire contenant les mots-clés
        :param limit: Nombre maximum de documents à retourner
        :return: Liste des documents correspondants
        """
        query = {key: {"$regex": value, "$options": "i"} for key, value in keywords.items()}
        return list(collection.find(query, {"_id": 0}).limit(limit))

    @staticmethod
    def fetch_general_books(limit=10):
        """
        Récupère un sous-ensemble de livres.
        :param limit: Nombre maximum de documents à retourner
        :return: Liste des documents
        """
        return list(collection.find({}, {"_id": 0, "Titre": 1, "Auteur": 1, "Specialite": 1, "Etas": 1}).limit(limit))
