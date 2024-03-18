import jwt
import datetime
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import get_user_model
from .models import Donateur,Administrateur
import logging

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return None

        try:
            token_type, token = authorization_header.split()
            
            if token_type != 'Bearer':
                raise exceptions.AuthenticationFailed('Invalid token type. Bearer token expected.')

            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except ValueError:
            raise exceptions.AuthenticationFailed('Invalid Authorization header. Token not found or incorrectly formatted.')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expiré. Veuillez vous reconnecter.')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Token invalide. Veuillez vous reconnecter.')

        user = Donateur.objects.filter(id_d=payload['id']).first()

        if user is None:
            raise exceptions.AuthenticationFailed('Utilisateur non trouvé.')

        return (user, None)

class AdminJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return None

        try:
            token_type, token = authorization_header.split()
            
            if token_type != 'Bearer':
                raise exceptions.AuthenticationFailed('Invalid token type. Bearer token expected.')

            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except ValueError:
            raise exceptions.AuthenticationFailed('Invalid Authorization header. Token not found or incorrectly formatted.')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expiré. Veuillez vous reconnecter.')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Token invalide. Veuillez vous reconnecter.')

        user = Administrateur.objects.filter(id=payload['id']).first()

        if user is None:
            raise exceptions.AuthenticationFailed('Utilisateur non trouvé.')

        return (user, None) 
def create_acces_token(id,prenom):
    payload = {
            'id': id,
            'prenom' : prenom,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
            'iat': datetime.datetime.utcnow(),
        }
    return jwt.encode(payload, 'secret', algorithm='HS256')
logger = logging.getLogger(__name__)

def create_refresh_token(id,prenom):
    payload = {
            'id': id,
            'prenom' : prenom,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
            'iat': datetime.datetime.utcnow(),
        }
    return jwt.encode(payload, 'secret', algorithm='HS256')
# class JWTAuthentication(BaseAuthentication):
#     def authenticate(self, request):
#         authorization_header = request.headers.get('Authorization')

#         if not authorization_header:
#             return None

#         try:
#             token_type, token = authorization_header.split()
            
#             if token_type != 'Bearer':
#                 raise exceptions.AuthenticationFailed('Invalid token type. Bearer token expected.')

#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            
#             # Récupérer le cookie JWT de la requête
#             cookie_token = request.COOKIES.get('jwt')
            
#             # Vérifier si le token JWT présenté correspond au token JWT stocké dans le cookie
#             if token != cookie_token:
#                 raise exceptions.AuthenticationFailed('Invalid token.')
                
#         except ValueError:
#             raise exceptions.AuthenticationFailed('Invalid Authorization header. Token not found or incorrectly formatted.')
#         except jwt.ExpiredSignatureError:
#             raise exceptions.AuthenticationFailed('Token expiré. Veuillez vous reconnecter.')
#         except jwt.InvalidTokenError:
#             raise exceptions.AuthenticationFailed('Token invalide. Veuillez vous reconnecter.')

#         user = get_user_model().objects.filter(id=payload['id']).first()

#         if user is None:
#             raise exceptions.AuthenticationFailed('Utilisateur non trouvé.')

#         return (user, None)