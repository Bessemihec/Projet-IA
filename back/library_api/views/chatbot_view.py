from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from ..repositories.chatbot_repository import chatbot_repository 
import openai
import json
import os

# Charger l'API key pour OpenAI
openai.api_key = "your key"  # Ajoutez OPENAI_API_KEY dans votre fichier .env
def is_booking_question(user_query):
    """
    Vérifie si la question de l'utilisateur est liée à la réservation de livres.
    """
    keywords = ["réserver un livre", "emprunter un livre", "prendre un livre", "comment réserver"]
    return any(keyword in user_query.lower() for keyword in keywords)
def generate_response(user_query, data):
    """
    Génère une réponse en utilisant l'API OpenAI.
    :param user_query: Question de l'utilisateur
    :param data: Données récupérées depuis MongoDB
    :return: Réponse générée par OpenAI
    """
    # Vérifier si l'intention est liée à la réservation
    if is_booking_question(user_query):
        return "Vous devez vous connecter à votre compte et accéder à la page détails du livre."
    prompt = f"""
    Tu es un assistant intelligent. Voici les livres disponibles :
    {json.dumps(data, ensure_ascii=False)}

    L'utilisateur a posé la question suivante : "{user_query}". Réponds clairement en utilisant les données fournies.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

class ChatbotView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return JsonResponse({"message": "Bonjour, je suis un assistant de bibliothèque digital. Comment puis-je vous aider ?"})
    def post(self, request):
        user_query = request.data.get("query", "")
        if not user_query:
            return Response({"error": "La requête utilisateur est vide."}, status=400)

        # Extraire les mots-clés (remplacez `extract_keywords` par votre propre fonction)
        keywords = {}  # Exemple : {"Titre": "Python", "Auteur": "Guido"}

        if keywords:
            books = chatbot_repository.fetch_books_by_keywords(keywords, limit=10)
        else:
            books = chatbot_repository.fetch_general_books(limit=10)

        chatbot_response = generate_response(user_query, books)
        return JsonResponse({"response": chatbot_response})
