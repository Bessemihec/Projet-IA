from library_api.repositories.book_repository import BookRepository
from library_api.repositories.user_repository import UserRepository
from library_project.settings import SECRET_KEY
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from library_api.serializers.book_serializer import BookSerializer
import jwt
import json


@csrf_exempt
def book_register(request):
    """
    Registers a new book.
    
    Method: POST
    Authorization: Bearer token required
    
    Body parameters:
    - title: str (required)
    - author: str (required)
    - link: str (required)
    - other fields from the Book model if needed

    Returns:
    - 201: Book created successfully
    - 400: Missing required fields or invalid JSON
    - 401: Token expired or invalid
    - 404: User not found
    - 500: Internal server error
    """
    if request.method == 'POST':
        token = request.headers.get('Authorization').split(' ')[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = payload['_id']

            user_repo = UserRepository()
            user_data = user_repo.get_user_by_id(user_id)

            if not user_data:
                return JsonResponse({'error': 'User not found'}, status=404)

            # Parse incoming data
            data = json.loads(request.body.decode('utf-8'))

            # Mapping incoming fields to the Book model fields
            book_data = {
                'Titre': data.get('title'),
                'Auteur': data.get('author'),
                'Code_barre': data.get('code_barre', None),
                'D_Object': data.get('d_object', None),
                'CREATION': data.get('creation', None),
                'MODIF': data.get('modif', None),
                'Cote': data.get('cote', None),
                'Inventaire': data.get('inventaire', None),
                'epn': data.get('epn', None),
                'Locale': data.get('locale', None),
                'Staff_Note': data.get('staff_note', None),
                'Public_Note': data.get('public_note', None),
                'ISBN_A': data.get('isbn_a', None),
                'ISBN_Z': data.get('isbn_z', None),
                'Item_class': data.get('item_class', None),
                'Specialite': data.get('specialite', None),
                'Nb_Page': data.get('nb_page', None),
                'Date_edition': data.get('date_edition', None),
                'Editeur': data.get('editeur', None),
                'Prix': data.get('prix', None),
                'post_by': user_id  # User who posts the book
            }

            # Check if essential fields are provided
            if not book_data['Titre'] or not book_data['Auteur']:
                return JsonResponse({'error': 'Missing required fields (title or author)'}, status=400)

            book_repo = BookRepository()
            book_created = book_repo.create_book(book_data)

            if book_created:
                return JsonResponse({'message': 'Book created successfully'}, status=201)
            else:
                return JsonResponse({'error': 'Failed to create book'}, status=500)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token has expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def get_books(request):
    """
    Retrieves a list of all books.
    
    Method: GET
    
    Returns:
    - 200: List of books
    - 500: Internal server error
    """
    if request.method == 'GET':
        try:
            book_data = BookRepository().get_books()
            serialized_books = [BookSerializer.serialize(book) for book in book_data]
            return JsonResponse(serialized_books, safe=False, status=200)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def book_info(request, _id):
    """
    Retrieves information about a specific book.
    
    Method: GET
    
    Path parameters:
    - _id: str (required)
    
    Returns:
    - 200: Book data
    - 404: Book not found
    - 500: Internal server error
    """
    if request.method == 'GET':
        try:
            book_repo = BookRepository()
            book_data = book_repo.get_book(_id)

            if book_data:
                serialized_book = BookSerializer.serialize(book_data)
                return JsonResponse(serialized_book, safe=False)
            else:
                return JsonResponse({'error': 'Book not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def book_update(request, book_id):
    """
    Updates information about a specific book.
    
    Method: PUT
    Authorization: Bearer token required
    
    Path parameters:
    - book_id: str (required)
    
    Body parameters (at least one required):
    - title: str
    - author: str
    - link: str

    Returns:
    - 200: Book updated successfully
    - 400: No fields provided for update or invalid JSON
    - 401: Token expired or invalid
    - 403: Unauthorized
    - 404: Book not found
    - 500: Internal server error
    """
    if request.method == 'PUT':
        token = request.headers.get('Authorization').split(' ')[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = payload['_id']

            book_repo = BookRepository()
            book_data = book_repo.get_book(book_id)

            if not book_data:
                return JsonResponse({'error': 'Book not found'}, status=404)

            if str(book_data['post_by']) != user_id:
                return JsonResponse({'error': 'Unauthorized'}, status=403)

            data = json.loads(request.body)

            # Ensure that at least one field is provided for update
            if not any(field in data for field in ['title', 'author', 'link']):
                return JsonResponse({'error': 'No fields provided for update'}, status=400)

            # Prepare the update data
            update_data = {key: value for key, value in data.items() if key in ['title', 'author', 'link']}
            
            # Update the book in the database
            result = book_repo.update_book(book_id, update_data)

            if result.modified_count > 0:
                # Fetch the updated book data to return
                updated_book = book_repo.get_book(book_id)
                serialized_book = BookSerializer.serialize(updated_book)
                return JsonResponse(serialized_book, safe=False)
            else:
                return JsonResponse({'error': 'Book not found or no changes made'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token has expired'}, status=401)
        
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


@csrf_exempt
def book_delete(request, book_id):
    """
    Deletes a specific book.
    
    Method: DELETE
    Authorization: Bearer token required
    
    Path parameters:
    - book_id: str (required)
    
    Returns:
    - 200: Book deleted successfully
    - 401: Token expired or invalid
    - 403: Unauthorized
    - 404: Book not found
    - 500: Internal server error
    """
    if request.method == 'DELETE':
        token = request.headers.get('Authorization').split(' ')[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = payload['_id']

            book_repo = BookRepository()
            book_data = book_repo.get_book(book_id)

            if not book_data:
                return JsonResponse({'error': 'Book not found'}, status=404)

            if str(book_data['post_by']) != user_id:
                return JsonResponse({'error': 'Unauthorized'}, status=403)

            result = book_repo.delete_book(_id = book_id)

            if result.deleted_count > 0:
                return JsonResponse({'message': 'Book deleted successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Book not found'}, status=404)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token has expired'}, status=401)
        
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)