# dans views.py
from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Wilaya, Type_Sang, Donateur,Administrateur
from .serializer import WilayaSerializer, Type_SangSerializer, DonateurSerializer,TestDonateurSerializer,AdminSerializer,Admin_DonateurSerializer,Affiche_DonateurSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
from django.contrib.auth import get_user_model
from dons_des_sangs.authen import JWTAuthentication,AdminJWTAuthentication,create_acces_token,create_refresh_token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .messageotp import MessageHandler
import random
from django.conf import settings

@api_view(['GET'])
def hell(request):
    return Response({'message': 'Hello, world!'})


class WilayaView(APIView):
    def get(self,request):
        wilayas = Wilaya.objects.all()
        serializer = WilayaSerializer(wilayas,many = True)
        return Response(serializer.data)
    def post(self,request):
        serializer = WilayaSerializer(data=request.data,many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data) 
    # @authentication_classes([JWTAuthentication])
    # @permission_classes([IsAuthenticated])
    def delete(self, request, nom):
        try:
            wilayas = Wilaya.objects.get(nom=nom)
        except wilayas.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        wilayas.delete()
        
        return Response(data={"message": f"Le type de sang {nom} a été supprimé avec succès."}, status=status.HTTP_200_OK)
    # @authentication_classes([JWTAuthentication])
    # @permission_classes([IsAuthenticated])
    def delete(self, request):
        # Supprimer toutes les wilayas
        Wilaya.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Type_SangSetview(APIView):
    def get(self,request):
        sang = Type_Sang.objects.all()
        serializer = Type_SangSerializer(sang,many = True)
        return Response(serializer.data)
    def post(self,request):
        serializer = Type_SangSerializer(data=request.data,many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data) 
    def delete(self, request):
        # Supprimer toutes les wilayas
        Wilaya.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def delete(self, request, nom):
        try:
            type_sang = Type_Sang.objects.get(nom=nom)
        except Type_Sang.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        type_sang.delete()
        
        return Response(data={"message": f"Le type de sang {nom} a été supprimé avec succès."}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    def post(self, request):
        serializer = DonateurSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class RegisterAdminView(APIView):
    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class ListeDonateur(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        Donateurs = Donateur.objects.filter(a_fait_don = False,test = False)
        serializer = DonateurSerializer(Donateurs,many=True)
        return Response(serializer.data)
    
class donateuradminview(APIView):
    def get(self, request):
        Donateurs = Donateur.objects.filter(a_fait_don=True)
        serializer = Affiche_DonateurSerializer(Donateurs, many=True)
        return Response(serializer.data)
class AdiminView(APIView):
    # uthentication_classes = [AdminJWTAuthentication]
    # permission_classes = [IsAuthenticated] 
    
    def get(self, request):
        Donateurs = Donateur.objects.filter(a_fait_don=False)
        serializer = Affiche_DonateurSerializer(Donateurs, many=True)
        return Response(serializer.data)

    
    def delete(self, request, id):
        try:
            donateur = Donateur.objects.get(id_d=id)
        except Donateur.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        donateur.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, id):
        try:
            donateur = Donateur.objects.get(id_d=id)
        except Donateur.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        test_value = request.data.get('test')
        serializer = TestDonateurSerializer(donateur, data={'test': test_value}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message': 'Le test du donateur a été mis à jour avec succès'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateDonateurStatus(APIView):
    def get(self, request):
        # Récupérer tous les donateurs avec a_fait_don = True
        donateurs = Donateur.objects.filter(a_fait_don=True)

        # Parcourir tous les donateurs et mettre à jour leur statut si nécessaire
        for donateur in donateurs:
            if donateur.a_fait_don and donateur.date_don_active <= datetime.date.today():
                donateur.a_fait_don = False
                donateur.date_don_active = None
                donateur.date_don = None
                donateur.save()

        # Retourner une réponse appropriée
        return Response({"message": "Statut des donateurs mis à jour avec succès."}, status=status.HTTP_200_OK)    
    
    
class DonateurSetview(APIView):
    def get(self, request,id):
        Donateurs = Donateur.objects.get(id_d=id)
        serializer = Affiche_DonateurSerializer(Donateurs)
        return Response(serializer.data)

# class DonateurUpdateView(APIView):
#     def put(self, request, pk):
#         try:
#             donateur = Donateur.objects.get(pk=pk)
#         except Donateur.DoesNotExist:
#             return Response({"message": "Donateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        
#         # Marquer le donateur comme ayant fait un don
#         donateur.a_fait_don = True
#         donateur.save()
        
#         serializer = Admin_DonateurSerializer(donateur)
#         return Response(serializer.data)
class DonateurUpdateView(APIView):
    def put(self, request, pk):
        try:
            # Récupérer le donateur à mettre à jour en fonction de pk
            donateur = Donateur.objects.get(pk=pk)
        except Donateur.DoesNotExist:
            return Response({"message": "Donateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        
        # Mettre à jour les données du donateur avec les nouvelles données envoyées dans la requête
        serializer = Admin_DonateurSerializer(donateur, data=request.data)
        if serializer.is_valid():
            # Récupérer la valeur de a_fait_don dans les données validées
            a_fait_don_value = request.data.get('a_fait_don')
            #a_fait_don = serializer.validated_data.get('a_fait_don', donateur.a_fait_don)

            if a_fait_don_value:
                # Si a_fait_don est True, affecter date_don à la date actuelle
                donateur.a_fait_don = a_fait_don_value
                donateur.date_don = datetime.date.today()
                donateur.date_don_active = donateur.date_don + datetime.timedelta(days=180)
            else:
                donateur.a_fait_don = a_fait_don_value
                # Si a_fait_don est False, mettre date_don à null
                donateur.date_don = None
                # Mettre date_don_active à null
                donateur.date_don_active = None
            
            # Sauvegarder les modifications
            donateur.save()
            
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
 
        # if not email or not password:
        #     raise AuthenticationFailed('Veuillez fournir à la fois l\'email et le mot de passe.')

        # Rechercher un utilisateur avec l'email fourni
        user = Donateur.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('L\'utilisateur n\'existe pas.')

        if not user.check_password(password):
            raise AuthenticationFailed('Le mot de passe est incorrect.')

        access_token = create_acces_token(user.id_d,user.first_name)
        refresh_token = create_refresh_token(user.id_d,user.first_name)
        
        response = Response({
            'token': access_token,
            'refresh': refresh_token
        })

        return response
    
class RefreshView(APIView):
    def post(self, request):
        refresh = request.data.get('refresh')

        if not refresh:
            raise AuthenticationFailed('Le token de rafraîchissement est manquant dans la requête.')

        try:
            payload = jwt.decode(refresh, 'secret', algorithms=['HS256'])
            access_token = create_acces_token(payload['id'],payload['prenom'])
            return Response({'token': access_token})
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Le token de rafraîchissement a expiré.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Le token de rafraîchissement est invalide.')

    
class LoginAdminView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            raise AuthenticationFailed('Veuillez fournir à la fois l\'email et le mot de passe.')

        # Rechercher un utilisateur avec l'email fourni
        user = Administrateur.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('L\'utilisateur n\'existe pas.')

        if not user.check_password(password):
            raise AuthenticationFailed('Le mot de passe est incorrect.')

        # Vérifier si l'utilisateur est un superutilisateur
        if not user.is_staff:
            raise AuthenticationFailed('Vous n\'avez pas les autorisations nécessaires pour vous connecter.')
        token = create_acces_token(user.id_A,user.first_name)
        refresh = create_refresh_token(user.id_A,user.first_name)
        
        response = Response({
            'access_token':token,
            'refresh_token' :refresh
        })
        

        return response


class UserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Utilisation correcte de IsAuthenticated

    def get(self, request):
        user = request.user
        if user.is_anonymous:
            return Response({'detail': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        donateur = user.donateur
        serializer = DonateurSerializer(donateur)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        if user.is_anonymous:
            return Response({'detail': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        donateur = user.donateur
        password = request.data.get('password')
        password_confirm = request.data.get('password_confirm')
        serializer = DonateurSerializer(donateur, data={'password': password, 'password_confirm': password_confirm}, partial=True)
        if serializer.is_valid():
            # Cryptage du mot de passe
            donateur.set_password(password)
            donateur.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class updatedonateurtest(APIView):   
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  
    def put(self, request):
        user = request.user
        if user.is_anonymous:
            return Response({'detail': 'Unauthenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        test_value = request.data.get('test')
        donateur = user.donateur
        serializer = TestDonateurSerializer(donateur, data={'test': test_value}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Le test du donateur a été mis à jour avec succès'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CountDonateur(APIView):
    def get(self, request):
        countD = Donateur.objects.count()
        countfd = Donateur.objects.filter(a_fait_don = True).count()
        countpr = Donateur.objects.filter(a_fait_don = False).count()
        countnpr = Donateur.objects.filter(a_fait_don = False,test = False).count()  
        return Response({
            'countD' : countD,
            'countfd': countfd,
            'countpr': countpr,
            'countnpr': countnpr
            
        })
    
class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            response = Response()
            response.delete_cookie('jwt')
            response.data = {
                'message': 'Déconnexion réussie.'
            }
            return response
        except Exception as e:
            response = Response()
            response.data = {
                'error': 'Une erreur est survenue lors de la déconnexion.'
            }
            return response


 
    
# class VerifyOTPView(viewsets.ModelViewSet):
#     def post(self, request):
#         email = request.data.get('email')
#         otp_entered = request.data.get('otp')
#         try:
#             profile = Profile.objects.get(email=email)
#         except Profile.DoesNotExist:
#             return Response({"error": "Aucun profil avec cet e-mail n'a été trouvé"}, status=status.HTTP_404_NOT_FOUND)
        
#         if profile.otp == otp_entered:
#             profile.is_verified = True
#             profile.save()
#             return Response({"message": "Votre compte a été activé avec succès"}, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Le code OTP est incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        
# class ProfileViewSet(viewsets.ModelViewSet):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)



#         otp = random.randint(1000, 9999)
#         serializer.save(otp=otp)

#         message_handler = MessageHandler(request.data.get('phone_number'), otp)
#         message_handler.send_otp_via_message()

#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
 # class LoginView(APIView):
#     authentication_classes = [] 
#     def post(self, request):
#         tel = request.data.get('tel')
#         email = request.data.get('email')  # Ajout de la prise en charge de l'email
#         password = request.data.get('password')

#         if not (tel or email) or not password:
#             raise AuthenticationFailed('Veuillez fournir à la fois le numéro de téléphone ou l\'email et le mot de passe.')

#         # Rechercher un utilisateur avec le numéro de téléphone ou l'email fourni
#         user = None
#         if tel:
#             user = get_user_model().objects.filter(tel=tel).first()
#         elif email:
#             user = get_user_model().objects.filter(email=email).first()

#         if user is None:
#             raise AuthenticationFailed('L\'utilisateur n\'existe pas.')

#         if not user.check_password(password):
#             raise AuthenticationFailed('Le mot de passe est incorrect.')
        
#         payload = {
#             'id': user.id,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#             'iat': datetime.datetime.utcnow(),
#         }
        
#         token = jwt.encode(payload, 'secret', algorithm='HS256')
#         response = Response() 
#         response.set_cookie(key='jwt', value=token, httponly=True)
#         response.data = {
#             'jwt': token
#         }
        
#         return response