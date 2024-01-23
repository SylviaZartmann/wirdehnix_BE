from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model

from django.contrib.auth.models import User

# wird in  RegisterView aufgerufen
def send_activationmail_to_user(new_user, token):
    confirmation_link = f"https://wirdehnix.sylviazartmann.de/confirm-registration/{token}" # Bestätigungslink erstellen
    message = f"Hi {new_user.username},\n\nPlease click the following link to activate your account:\n{confirmation_link}"
    send_mail(
        "Account Activation",
        message,
        "contact@sylviazartmann.de",
        [new_user.email],
        fail_silently=False,
    )
    
    
# wird in Urls aufgerufen    
@api_view(('GET', )) # wir haben einen Get Request aus dem Frontend
@permission_classes((AllowAny,))
def activate_user(request, token):
    user = get_object_or_404(User, auth_token=token)
    user.is_active = True
    user.save()
    return Response({'message': 'User activated successfully.'})    
    
    
# wird im LoginSerializer aufgerufen    
def gibbet_den_user(email, password):
    try: 
        user = get_user_model().objects.get(email=email) # wir holen uns den user anhand der vorhandenen email
        if user.check_password(password): # wir überprüfen das passwort mit dem vorhandenen passwort
            return user # wir geben den user als solchen zurück, weil passt
    except get_user_model().DoesNotExist:
        return None