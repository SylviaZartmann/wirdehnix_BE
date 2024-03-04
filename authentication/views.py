from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from authentication.serializer import LoginSerializer, RegisterSerializer
from . import utils

@permission_classes((AllowAny,))
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = get_user_model().objects.get(email=serializer.validated_data['email'])
            token, created = Token.objects.get_or_create(user=user)
            utils.send_activationmail_to_user(user, token)
            return Response({'username': user.username, 'email': user.email, 'token': token.key}, status=status.HTTP_201_CREATED)
                 
        if 'username'in serializer.errors: 
            return Response('Username already exists!', status=status.HTTP_400_BAD_REQUEST)
        if "email" in serializer.errors:
            return Response('Email already exists!', status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LoginView(ObtainAuthToken): 
    
    serializer_class = LoginSerializer
    
    def post(self, request):
        
        serializer = self.serializer_class(data=request.data)
                 
        if serializer.is_valid(raise_exception=True):
            userData = serializer.validated_data
            email = userData.get('email')
            
            if email: 
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
                            
                            
        else: 
            email = serializer.data.get('email')
            if not email: 
                return Response('Email is missing!', status=status.HTTP_400_BAD_REQUEST)
        
            try:
                user = get_user_model().objects.get(email=email)
            
                if not user.is_active:
                    return Response('Email not activated!', status=status.HTTP_403_FORBIDDEN)
            
            except get_user_model().DoesNotExist:
                return Response('User not born yet!', status=status.HTTP_404_NOT_FOUND)
            return Response('Invalid data', status=status.HTTP_400_BAD_REQUEST)                

@permission_classes((IsAuthenticated,)) 
@authentication_classes((TokenAuthentication,)) 
class LogoutView(APIView):
    
    def post(self, request):
                
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