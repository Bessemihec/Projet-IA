from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden, JsonResponse
from library_api.repositories.user_repository import UserRepository
from library_api.serializers.user_serializer import UserSerializer
from library_project.settings import SECRET_KEY
import jwt
import bcrypt
import qrcode
from io import BytesIO
from base64 import b64encode


@csrf_exempt
def user_register(request):
    """
    Registers a new user.

    Method: POST
    Body: JSON containing 'email', 'role', 'password', and optionally 'university' and 'speciality' for students

    Returns:
        201: User created successfully
        400: User creation failed (e.g., email already exists or invalid JSON)
        405: Invalid request method
        500: Internal server error
    """
    if request.method == 'POST':
        try:
            # Désérialiser les données du corps de la requête
            data = UserSerializer.deserialize(request.body.decode('utf-8'))
            email = data.get('email')
            role = data.get('role')
            password = data.get('password')

            # Récupérer les données supplémentaires pour les étudiants
            university = data.get('university') if role == 'étudiant' else None
            speciality = data.get('speciality') if role == 'étudiant' else None

            user_repository = UserRepository()

            # Appeler la méthode create_user du repository
            user_created = user_repository.create_user(
                email=email,
                username=data.get('username'),  # Assurez-vous que 'username' est bien dans les données
                password=password,
                role=role,
                university=university,  # Passer university pour les étudiants
                speciality=speciality    # Passer speciality pour les étudiants
            )

            if user_created:
                return JsonResponse({'message': 'User created successfully'}, status=201)
            else:
                return JsonResponse({'message': 'User creation failed: Email already exists'}, status=400)

        except ValueError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'message': f'An error occurred: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Invalid request method'}, status=405)


@csrf_exempt
def user_login(request):

    """
    Logs in a user.

    Method: POST
    Body: JSON containing 'email' and 'password' or 'qr_code'

    Returns:
        200: JWT token
        400: Invalid JSON
        403: Invalid credentials
        405: Invalid request method
        500: Internal server error
    """

    if request.method == 'POST':
        try:
            data = UserSerializer.deserialize(request.body.decode('utf-8'))
            email = data.get('email')
            password = data.get('password')
            qr_code = data.get('qr_code')

            user_repo = UserRepository()

            if qr_code:
                user_data = user_repo.get_user_by_qr_code(qr_code)
                if user_data:
                    payload = {
                        '_id': str(user_data.get('_id')),
                        'role': user_data.get('role'),
                        'exp': datetime.utcnow() + timedelta(days=1)  # Token expiration time
                    }
                    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
                    return JsonResponse({'token': token}, status=200)
                else:
                    return HttpResponseForbidden('Invalid QR code')

            if email and password:
                user_data = user_repo.get_user_by_email(email)

                if user_data:
                    stored_password = user_data.get('password')
                    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                        payload = {
                            '_id': str(user_data.get('_id')),
                            'role': user_data.get('role'),
                            'exp': datetime.utcnow() + timedelta(days=1)  # Token expiration time
                        }
                        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
                        return JsonResponse({'token': token}, status=200)
                    else:
                        return HttpResponseForbidden('Invalid credentials')
                else:
                    return HttpResponseForbidden('Invalid credentials')
            else:
                return JsonResponse({'error': 'Email and password or QR code required'}, status=400)

        except ValueError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def user_delete(request, _id):
    """
    Deletes a user based on their user ID.

    Method: DELETE
    Header: Authorization token

    Returns:
        200: User deleted successfully
        403: User not found or token invalid
        405: Invalid request method
    """

    if request.method == 'DELETE':
        token = request.headers.get('Authorization').split(' ')[1]  # Récupérer le token JWT

        try:
            # Décodage du token pour récupérer les informations de l'utilisateur
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            logged_in_user_id = payload['_id']  # ID de l'utilisateur connecté

            user_repo = UserRepository()
            user_data = user_repo.get_user_by_id(_id)

            if user_data:
                # Suppression de l'utilisateur
                user_repo.delete_user(_id)
                return JsonResponse({'message': 'User deleted successfully'})
            else:
                return HttpResponseForbidden('User not found')

        except jwt.ExpiredSignatureError:
            return HttpResponseForbidden('Token expired')
        except jwt.InvalidTokenError:
            return HttpResponseForbidden('Invalid token')

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def user_update(request, _id):
    """
    Updates a user's information based on their user ID.

    Method: PUT
    Header: Authorization token
    Body: JSON containing 'email', 'role', and/or 'password'

    Returns:
        200: User updated successfully
        403: User not found or token invalid
        405: Invalid request method
    """

    if request.method == 'PUT':
        token = request.headers.get('Authorization').split(' ')[1]  # Récupérer le token JWT

        try:
            # Décodage du token pour récupérer les informations de l'utilisateur
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            logged_in_user_id = payload['_id']  # ID de l'utilisateur connecté

            user_repo = UserRepository()
            user_data = user_repo.get_user_by_id(_id)

            if user_data:
                # Désérialisation des données envoyées dans le corps de la requête
                data = UserSerializer.deserialize(request.body.decode('utf-8'))
                
                # Seules ces informations peuvent être mises à jour
                new_username = data.get('username')
                new_email = data.get('email')
                new_university = data.get('university')
                new_speciality = data.get('speciality')

                # Mise à jour uniquement des champs autorisés
                if new_username:
                    user_data['username'] = new_username
                if new_email:
                    user_data['email'] = new_email
                if new_university:
                    user_data['university'] = new_university
                if new_speciality:
                    user_data['speciality'] = new_speciality

                # Mise à jour de l'utilisateur
                user_repo.update_user(_id, user_data)
                return JsonResponse({'message': 'User updated successfully'})
            else:
                return HttpResponseForbidden('User not found')

        except jwt.ExpiredSignatureError:
            return HttpResponseForbidden('Token expired')
        except jwt.InvalidTokenError:
            return HttpResponseForbidden('Invalid token')

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def user_info(request):

    """
    Retrieves a user's information.

    Method: GET
    Header: Authorization token

    Returns:
        200: User information
        403: User not found or token invalid
        405: Invalid request method
    """

    if request.method == 'GET':
        token = request.headers.get('Authorization').split(' ')[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            _id = payload['_id']
            user_data = UserRepository().get_user_by_id(_id)

            if user_data:
                user_data = UserSerializer.sanitize(user_data)
                user_data['_id'] = str(user_data['_id'])
                return JsonResponse(user_data)
            else:
                return HttpResponseForbidden('User not found')
        except jwt.ExpiredSignatureError:
            return HttpResponseForbidden('Token expired')
        except jwt.InvalidTokenError:
            return HttpResponseForbidden('Invalid token')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def user_open_info(request, _id):
    
    """
    Get user information by user ID.

    Args:
        request (HttpRequest): The request object.
        _id (str): The user ID.

    Returns:
        JsonResponse: User information JSON response.
        HttpResponseForbidden: Forbidden response if user not found or token expired/invalid.
    """
     
    if request.method == 'GET':
        try:
            user_data = UserRepository().get_user_by_id(_id)

            if user_data:
                user_data = UserSerializer.sanitize(user_data)
                user_data['_id'] = str(user_data['_id'])
                return JsonResponse(user_data)
            else:
                return HttpResponseForbidden('User not found')
        except jwt.ExpiredSignatureError:
            return HttpResponseForbidden('Token expired')
        except jwt.InvalidTokenError:
            return HttpResponseForbidden('Invalid token')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

# Function to generate a QR code for user authentication
def generate_qr_code(user_id, email, role):
    """
    Génère un QR code basé sur l'adresse e-mail et le rôle de l'utilisateur.

    Args:
        user_id (str): L'identifiant de l'utilisateur.
        email (str): L'adresse e-mail de l'utilisateur.
        role (str): Le rôle de l'utilisateur (étudiant, bibliothécaire, administrateur).

    Returns:
        JsonResponse: Une réponse contenant le QR code encodé en base64.
    """
    try:
        # Déterminer la durée de validité selon l'adresse e-mail
        if "@ihec.ucar.tn" in email:
            expiration = timedelta(days=365)  # 1 an
        else:
            expiration = timedelta(days=1)  # 24 heures

        # Créer un payload pour le JWT
        payload = {
            'user_id': user_id,
            'email': email,
            'role': role,
            'exp': datetime.utcnow() + expiration  # Date d'expiration
        }

        # Générer le JWT
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # Créer un QR Code contenant le token
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(token)
        qr.make(fit=True)

        # Générer l'image du QR Code
        img = qr.make_image(fill='black', back_color='white')

        # Convertir l'image en base64
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        img_base64 = b64encode(img_io.getvalue()).decode('utf-8')

        # Retourner le QR Code encodé et le token
        return JsonResponse({'qr_code': img_base64, 'token': token})
    except Exception as e:
        return JsonResponse({'error': f'Erreur lors de la génération du QR Code : {str(e)}'}, status=500)
    # Ajoutez la vue pour générer le QR Code
@csrf_exempt
def generate_user_qr_code(request):
    """
    Génère un QR Code pour un utilisateur basé sur son e-mail et son rôle.

    Méthode: GET
    Paramètres : user_id (str), email (str), role (str)
    """
    if request.method == 'GET':
        try:
            user_id = request.GET.get('user_id')
            email = request.GET.get('email')
            role = request.GET.get('role')

            if not user_id or not email or not role:
                return JsonResponse({'error': 'Les paramètres user_id, email et role sont requis'}, status=400)

            # Générer le QR Code pour cet utilisateur
            return generate_qr_code(user_id, email, role)

        except Exception as e:
            return JsonResponse({'error': f'Erreur lors de la génération du QR Code : {str(e)}'}, status=500)

    else:
        return JsonResponse({'error': 'Méthode HTTP non autorisée'}, status=405)
    
@csrf_exempt
def get_all_users(request):
    """
    Récupère la liste de tous les utilisateurs.

    Méthode: GET
    En-tête: Token d'authentification

    Returns:
        200: Liste des utilisateurs
        403: Token invalide ou expiré
        405: Méthode non autorisée
    """
    if request.method == 'GET':
        token = request.headers.get('Authorization')

        if not token:
            return JsonResponse({'error': 'Token d\'authentification requis'}, status=403)

        try:
            # Vérifier et décoder le token JWT
            payload = jwt.decode(token.split(' ')[1], SECRET_KEY, algorithms=['HS256'])
            user_repo = UserRepository()
            users = user_repo.get_all_users()

            # Si des utilisateurs sont trouvés
            if users:
                # Sérialiser et envoyer les données des utilisateurs
                users_data = [UserSerializer.sanitize(user) for user in users]
                for user in users_data:
                    user['_id'] = str(user['_id'])
                return JsonResponse({'users': users_data}, status=200)
            else:
                return JsonResponse({'message': 'Aucun utilisateur trouvé'}, status=404)

        except jwt.ExpiredSignatureError:
            return HttpResponseForbidden('Token expiré')
        except jwt.InvalidTokenError:
            return HttpResponseForbidden('Token invalide')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Méthode HTTP non autorisée'}, status=405)
