import bcrypt
from bson import ObjectId
from library_project.settings import *
import qrcode
import jwt
from datetime import datetime, timedelta
from io import BytesIO
from base64 import b64encode
from base64 import b64decode
from library_project.settings import SECRET_KEY

class UserRepository:
    def __init__(self):
        """
        Initialize a new UserRepository instance.
        Sets up the database client, database, and collection for users.
        """
        self.client = client
        self.db = db
        self.collection = self.db['users']

    def generate_qr_code(self, user_id, email, role):
        """
        Generate a QR code containing a JWT token for the user.

        Args:
            user_id (str): The user's ID.
            email (str): The user's email.
            role (str): The user's role.

        Returns:
            str: The QR code as a base64 string.
        """
        try:
            # Determine the expiration based on the email domain
            if "@ihec.ucar.tn" in email:
                expiration = timedelta(days=365)  # 1 year for IHEC students
            else:
                expiration = timedelta(days=1)  # 1 day for others

            # Create a JWT payload
            payload = {
                'user_id': user_id,
                'email': email,
                'role': role,
                'exp': datetime.utcnow() + expiration
            }

            # Encode the payload into a JWT token
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            # Create a QR code with the JWT token
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(token)
            qr.make(fit=True)

            # Generate the QR code image
            img = qr.make_image(fill='black', back_color='white')

            # Convert the image to base64
            img_io = BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)
            img_base64 = b64encode(img_io.getvalue()).decode('utf-8')

            return img_base64  # Return the QR code as a base64 string
        except Exception as e:
            return str(e)

    def create_user(self, email, username, password, role, university=None, speciality=None):
        """
        Create a new user in the database.
        The role is provided as a parameter and is independent of the email domain.
        QR code is generated and added to the user data.
        """
        existing_user = self.collection.find_one({'email': email})
        if existing_user:
            return False

        # Determine QR duration based on email domain
        if email.endswith("@ihec.ucar.tn"):
            qr_duration = 365 * 24  # 1 year for IHEC students
        else:
            qr_duration = 24  # 24 hours for non-IHEC students

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_data = {
            'email': email,
            'username': username,
            'password': hashed_password.decode('utf-8'),
            'role': role,
            'qr_duration': qr_duration  # Set QR duration based on email domain
        }

        # Add additional user data if role is "étudiant"
        if role == "étudiant":
            user_data['university'] = university
            user_data['speciality'] = speciality

        # Insert the user into the database
        result = self.collection.insert_one(user_data)
        
        if result.acknowledged:
            # Generate the QR code for the new user after insertion
            qr_code = self.generate_qr_code(str(result.inserted_id), email, role)
            
            # Update the user document with the QR code
            self.collection.update_one(
                {'_id': result.inserted_id},
                {'$set': {'qr_code': qr_code}}
            )

        return result.acknowledged

    def get_user_by_qr_code(self, qr_code):
        """
        Cette méthode cherche l'utilisateur dans la base de données en utilisant le QR code.

        Args:
            qr_code (str): Le QR code envoyé par l'utilisateur.

        Returns:
            dict: Les données de l'utilisateur si le QR code est trouvé dans la base de données.
            None: Si aucun utilisateur n'est trouvé.
        """
        try:
            # Cherche l'utilisateur en fonction du QR code
            user_data = self.collection.find_one({"qr_code": qr_code})
            return user_data
        except Exception as e:
            print(f"Erreur lors de la recherche de l'utilisateur par QR code : {str(e)}")
            return None
        
    def get_user_by_email(self, email):
        """
        Get a user by their email address from the database.
        """
        user_data = self.collection.find_one({'email': email})
        if user_data:
            return user_data
        return None
    
    def get_user_by_id(self, _id):
        """
        Get a user by their ID from the database.
        """
        user_data = self.collection.find_one({'_id': ObjectId(_id)})
        if user_data:
            return user_data
        return None

    def delete_user(self, _id):
        """
        Delete a user from the database.
        """
        result = self.collection.delete_one({'_id': ObjectId(_id)})
        return result.deleted_count > 0

    def update_user(self, _id, new_data):
        """
        Update a user in the database.
        """
        result = self.collection.update_one({'_id': ObjectId(_id)}, {'$set': new_data})
        return result.modified_count > 0
    def get_all_users(self):
        """
        Retrieves all users from the database.
        """
        return list(self.collection.find())  # Retourne tous les utilisateurs