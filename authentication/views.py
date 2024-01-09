from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.serializer import RegisterSerializer

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from . import utils
class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() # das erste, weil sonst nicht validated_data verarbeitet werden kann
            user = get_user_model().objects.get(email=serializer.validated_data['email'])
            token, created = Token.objects.get_or_create(user=user)
        #    utils.send_activationmail_to_user(serializer.validated_data, token)
            
            return Response({'username': user.username, 'email': user.email, 'token': token.key}, status=status.HTTP_201_CREATED)
                 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LoginView(APIView):
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = None
        if '@' in email:
            try:
                user = User.objects.get(email=email)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(email=email, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)    
    

@permission_classes([IsAuthenticated])
class LogoutView(APIView):
    
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)