from django.core.mail import send_mail
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def send_activationmail_to_user(new_user, token):
    confirmation_link = f"https://wirdehnix.sylviazartmann.de/confirm-registration/{token}"

    message = f"Hi {new_user.username},\n\nPlease click the following link to activate your account:\n{confirmation_link}"
    send_mail(
        "Account Activation",
        message,
        "contact@sylviazartmann.de",
        [new_user.email],
        fail_silently=False,
    )
    
   
@api_view(('GET', )) 
@permission_classes((AllowAny,))
def activate_user(request, token):
    user = get_object_or_404(User, auth_token=token)
    user.is_active = True
    user.save()
    return Response({'message': 'User activated successfully.'})    
    
    
    
def gibbet_den_user(email, password):
    try: 
        user = get_user_model().objects.get(email=email) 
        if user.check_password(password):
            return user 
    except get_user_model().DoesNotExist:
        return None

@api_view(('POST', )) 
@permission_classes((AllowAny,))
def send_pw_reset_mail(request):
    try:
        email = request.data.get('email')
        user = get_user_model().objects.get(email=email)
    except ObjectDoesNotExist:
        raise Response('User not found!', status=status.HTTP_404_NOT_FOUND)
        
    token = Token.objects.get_or_create(user=user)
    
    reset_link = f"https://wirdehnix.sylviazartmann.de/changePW/confirm/{token[0]}"
    message = f"Hi {user.username},\n\nPlease click the following link to reset your password:\n{reset_link}"
    send_mail(
        "Change Password",
        message,
        "contact@sylviazartmann.de",
        [email],
    )
    return Response({'message': 'Password reset link sent successfully.'})
    
    
@api_view(('POST', )) 
@permission_classes((AllowAny,))
def change_password(request, **kwargs):
    try:
        token = kwargs.get('token')
        new_pw = request.data.get('password')
        new_confpw = request.data.get('conf_password') 

        if new_pw != new_confpw:
            raise ValidationError("Mismatched passwords.")

        user = get_object_or_404(User, auth_token=token)
        user.set_password(new_pw)
        user.save()

        return Response({'message': 'Password changed successfully.'})
    
    except get_user_model().DoesNotExist:
        raise ValidationError("Invalid token or user not found.")
    
    except Exception as e:
        raise ValidationError(f"An error occurred: {str(e)}")