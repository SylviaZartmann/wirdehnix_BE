from django.contrib.auth.models import User
from django.contrib.auth import logout, get_user_model, authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from authentication.serializer import LoginSerializer, RegisterSerializer
from . import utils


class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() # das erste, weil sonst nicht validated_data verarbeitet werden kann
            user = get_user_model().objects.get(email=serializer.validated_data['email'])
            token, created = Token.objects.get_or_create(user=user)
        #    utils.send_activationmail_to_user(serializer.validated_data, token)
        #    active User muss noch ausgeführt werden, um den User zu aktivieren nach der Mail
            return Response({'username': user.username, 'email': user.email, 'token': token.key}, status=status.HTTP_201_CREATED)
                 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LoginView(ObtainAuthToken): # ObtainAuthToken, generiert in dieser ansicht automatisch einen token
    
    serializer_class = LoginSerializer
    
    def post(self, request):
        
        serializer = self.serializer_class(data=request.data)
                 
        if serializer.is_valid(raise_exception=True):
            userData = serializer.validated_data
            email = userData.get('email')
            
            if email: # wir haben eine valide email adresse hie 
                try:
                    user = get_user_model().objects.get(email=userData['email'])
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({
                        'token': token.key,
                        'user_id': user.pk,
                        'email': user.email
                    })
                except get_user_model().DoesNotExist:
                    return Response('User not born yet!', status=status.HTTP_404_NOT_FOUND)
            else:
                return Response('Email for the ass!', status=status.HTTP_400_BAD_REQUEST)
                            
                            
        else: # das ist der Teil, wenn serializer is nicht valid! Warum auch immer .. 
            email = serializer.data.get('email')
            if not email: # hier sieht marijan probleme, weil not statt nix
                return Response('Email is missing!', status=status.HTTP_400_BAD_REQUEST)
        
            try:
                user = get_user_model().objects.get(email=email)
            
                if not user.is_active:
                    return Response('Email not activated!', status=status.HTTP_403_FORBIDDEN)
            
            except get_user_model().DoesNotExist:
                return Response('User not born yet!', status=status.HTTP_404_NOT_FOUND)
            return Response('Invalid data', status=status.HTTP_400_BAD_REQUEST)                

@permission_classes((IsAuthenticated,)) # Copilot sagt, macht Sinn, weil mans sonst gar nicht sehen kann
@authentication_classes((TokenAuthentication,)) 
class LogoutView(APIView):
    
    def post(self, request):
        #token soll im header gesendet werden ?!
        # bei  Postman in den Header geschrieben und logout successfull bekommen
        # wie krieg ich den header jetzt hier rein? - gar nicht
        # token muss bei jeder Anfrage mitgeschickt werden, damit der User authentifiziert werden kann
                
        try:
            user = request.user
            print(user.is_authenticated)
            user_instance = get_user_model().objects.get(auth_token=user.auth_token)
            
            if user and user.is_active:
                try:
                    if hasattr(user_instance, 'auth_token'):
                        user_instance.auth_token.delete()
                    return Response('Successfully logged out.', status=status.HTTP_200_OK)    
                except user_instance.DoesNotExist:
                    return Response('User not born yet!', status=status.HTTP_404_NOT_FOUND)
                
            else:
                return Response('User not logged in.', status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print(f"Exception: {str(e)}")
            return Response('Internal Server Error', status=status.HTTP_500_INTERNAL_SERVER_ERROR)