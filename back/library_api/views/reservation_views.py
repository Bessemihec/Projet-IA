import json
import jwt
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from library_api.repositories.reservation_repository import ReservationRepository
from library_api.serializers.reservation_serializer import ReservationSerializer
from library_project.settings import SECRET_KEY

@csrf_exempt
def create_reservation(request):
    """
    Crée une nouvelle réservation.

    Méthode: POST
    Autorisation: Token JWT requis

    Paramètres du corps :
    - book_id: str (obligatoire)
    - duration: str (obligatoire)  # Durée de la réservation, ex: "7 days"
    - student_id: str (obligatoire)  # ID de l'étudiant (manuellement fourni pour les tests)

    Retourne :
    - 201: Réservation créée avec succès
    - 400: Champs requis manquants ou JSON invalide
    - 500: Erreur serveur interne
    """
    if request.method == 'POST':
        token = request.headers.get('Authorization')  # Récupère le token d'autorisation

        if not token:
            return JsonResponse({'error': 'Token requis'}, status=401)

        try:
            # Retirer le préfixe 'Bearer ' du token
            token = token.split(' ')[1]
            # Décoder le token
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            # Utiliser le student_id venant du token (mais on permet d'utiliser un autre student_id dans la requête)
            # student_id = payload['_id']  # Si nécessaire, on peut l'utiliser plus tard

        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Le token a expiré'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Token invalide'}, status=401)
        except Exception as e:
            return JsonResponse({'error': f'Une erreur est survenue lors de la vérification du token: {str(e)}'}, status=500)

        # Si le token est valide, récupérer les données de la requête
        try:
            data = json.loads(request.body.decode('utf-8'))
            book_id = data.get('book_id')
            duration = data.get('duration')
            student_id_request = data.get('student_id')  # ID de l'étudiant fourni dans la requête

            # Vérifiez que tous les champs sont présents
            if not book_id or not duration or not student_id_request:
                return JsonResponse({'error': 'Champs requis manquants'}, status=400)

            # Créer la réservation
            reservation_repo = ReservationRepository()
            reservation_created = reservation_repo.create_reservation(book_id=book_id, student_id=student_id_request, duration=duration)

            if reservation_created:
                return JsonResponse({'message': 'Réservation créée avec succès', 'duration': duration}, status=201)
            else:
                return JsonResponse({'error': 'Échec de la création de la réservation'}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON invalide'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Une erreur est survenue : {str(e)}'}, status=500)

    return JsonResponse({'error': 'Méthode HTTP invalide'}, status=405)

def get_reservations(request):
    """
    Récupère la liste de toutes les réservations.
    Méthode: GET
    Retourne :
    - 200: Liste des réservations
    - 500: Erreur serveur interne
    """
    if request.method == 'GET':
        try:
            reservation_data = ReservationRepository().get_reservations()  # Récupère toutes les réservations
            serialized_reservations = [ReservationSerializer.serialize(reservation) for reservation in reservation_data]
            return JsonResponse(serialized_reservations, safe=False, status=200)  # Retourne les réservations en JSON
        except Exception as e:
            return JsonResponse({'error': f'Une erreur est survenue : {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Méthode HTTP invalide'}, status=405)


def get_reservation(request, reservation_id):
    """
    Récupère les informations d'une réservation spécifique.

    Méthode: GET

    Paramètre :
    - reservation_id: str (obligatoire)

    Retourne :
    - 200: Détails de la réservation
    - 404: Réservation non trouvée
    - 500: Erreur serveur interne
    """
    if request.method == 'GET':
        try:
            reservation_repo = ReservationRepository()
            reservation_data = reservation_repo.get_reservation(reservation_id)

            if reservation_data:
                serialized_reservation = ReservationSerializer.serialize(reservation_data)
                return JsonResponse(serialized_reservation, safe=False)
            else:
                return JsonResponse({'error': 'Réservation non trouvée'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def update_reservation(request, reservation_id):
    """
    Met à jour une réservation spécifique.

    Méthode: PUT
    Autorisation: Token Bearer requis

    Paramètres du corps :
    - status: str (optionnel)  # Par exemple "completed", "pending", ou "in_progress"
    - duration: str (optionnel)  # Durée de la réservation sous forme de chaîne (ex: "2 hours", "3 days")

    Retourne :
    - 200: Réservation mise à jour avec succès
    - 400: JSON invalide ou champ requis manquant
    - 401: Token expiré ou invalide
    - 404: Réservation non trouvée
    - 500: Erreur serveur interne
    """
    if request.method == 'PUT':
        token = request.headers.get('Authorization').split(' ')[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            data = json.loads(request.body.decode('utf-8'))

            # Récupération des champs optionnels
            status = data.get('status')
            duration = data.get('duration')

            if not status and not duration:
                return JsonResponse({'error': 'Aucun champ à mettre à jour'}, status=400)

            reservation_repo = ReservationRepository()
            reservation_data = reservation_repo.get_reservation(reservation_id)

            if not reservation_data:
                return JsonResponse({'error': 'Réservation non trouvée'}, status=404)

            # Préparer les champs à mettre à jour
            update_fields = {}

            if status:
                update_fields['status'] = status
            if duration:  # Si la durée est modifiée, on met à jour la date de fin
                update_fields['duration'] = duration
                # Calculer la nouvelle date de fin en fonction de la nouvelle durée
                new_end_date = reservation_repo.calculate_end_date(duration)
                update_fields['date_fin_reservation'] = new_end_date

            # Mise à jour de la réservation
            result = reservation_repo.update_reservation(reservation_id, update_fields)

            if result.modified_count > 0:
                updated_reservation = reservation_repo.get_reservation(reservation_id)
                serialized_reservation = ReservationSerializer.serialize(updated_reservation)
                return JsonResponse(serialized_reservation, safe=False)
            else:
                return JsonResponse({'error': 'Aucune mise à jour effectuée'}, status=500)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Le token a expiré'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Token invalide'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON invalide'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Une erreur est survenue : {str(e)}'}, status=500)

    return JsonResponse({'error': 'Méthode HTTP invalide'}, status=405)





@csrf_exempt
def delete_reservation(request, reservation_id):
    """
    Supprime une réservation spécifique.

    Méthode: DELETE
    Autorisation: Token Bearer requis

    Retourne :
    - 200: Réservation supprimée avec succès
    - 401: Token expiré ou invalide
    - 404: Réservation non trouvée
    - 500: Erreur serveur interne
    """
    if request.method == 'DELETE':
        token = request.headers.get('Authorization').split(' ')[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            # On ne vérifie plus l'ID de l'étudiant
            # student_id = payload['_id']  # ID de l'étudiant connecté

            reservation_repo = ReservationRepository()
            reservation_data = reservation_repo.get_reservation(reservation_id)

            if not reservation_data:
                return JsonResponse({'error': 'Réservation non trouvée'}, status=404)

            # Suppression de la vérification de l'ID de l'utilisateur
            result = reservation_repo.delete_reservation(reservation_id)

            if result.deleted_count > 0:
                return JsonResponse({'message': 'Réservation supprimée avec succès'}, status=200)
            else:
                return JsonResponse({'error': 'Échec de la suppression de la réservation'}, status=500)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Le token a expiré'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Token invalide'}, status=401)
        except Exception as e:
            return JsonResponse({'error': f'Une erreur est survenue : {str(e)}'}, status=500)

    return JsonResponse({'error': 'Méthode HTTP invalide'}, status=405)
