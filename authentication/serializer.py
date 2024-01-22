from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from . import utils

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, min_length=8)
    conf_password = serializers.CharField(write_only=True)
    
    class Meta: 
        model = get_user_model()   
        fields = ('username', 'email', 'password', 'conf_password')
        
    def validation(self, value):
        
        username = value['username']
        if get_user_model().objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exists!')
       
        email = value['email']   
        try:
            validate_email(email) # Django built in Funktion, überprüft, ob valide Email Addresse
        except ValidationError: 
            raise serializers.ValidationError('Email address invalid!')
        if get_user_model().objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists!')
    
        password = value['password'] 
        conf_password = value['conf_password']
        
        if password != conf_password:
            raise serializers.ValidationError('No matching passwords!')
        
        else:
            try: 
                validate_password(password) # Django built in Funktion, überprüft, ob das Passwort den Sicherheitsrichtlinien entspricht
            except ValidationError: # Hier wird die Ausnahme abgefangen, falls das Passwort nicht den Anforderungen entspricht
                raise serializers.ValidationError('Password insecure!') # Wenn ValidationError, wird entsprechende Fehlermeldung über Serialisierer zurückgegeben. bedeutet, das Passwort nicht sicher
            
        return value # Wenn Passwort den Anforderungen entspricht, wird das ursprüngliche Passwort zurückgegeben.
        
    def create(self, valid_data):
        del valid_data["conf_password"]
        new_user = get_user_model().objects.create(**valid_data)
        new_user.set_password(valid_data["password"])
        new_user.is_active = False
        new_user.save()
        
        return new_user
    


# class ActivateUserSerializer(serializers.Serializer): # gibt dir mehr Flexibilität, ermöglicht es, benutzerdefinierte Validierungslogik ohne die automatische Modellerstellungsfunktionalität bereitzustellen       
#     token = serializers.CharField() # vorübergehend ein Feld erstellen, was es danach so nicht mehr gibt
        
#     def val_token(self, value):
            
#         for new_user in get_user_model().objects.filter(is_active=False): # in vorheriger Funktion eingefügt
#             if default_token_generator.check_token(new_user, value): # wir checken in den Benutzern, ob das übergebene Token mit einem vorhandenen Token übereinstimmt
#                 new_user.is_active = True # trifft es einen Token, wird is_active auf True gesetzt
#                 new_user.save() # die Änderungen werden gespeichert
#                 return value # geben alles zurück
            
#         raise serializers.ValidationError("Token provided is invalid!") # wenn kein passender Benutzer gefunden wird, gibts nen Fehler
        

class LoginSerializer(serializers.Serializer): # wir wollen mit email und passwort einloggen
    email = serializers.EmailField(required=True) # vorübergehend vorhandene Daten, die nicht gespeichert werden, nur abgeglichen
    password = serializers.CharField(write_only=True, required=True)
      
    def validate(self, data):
        user = utils.gibbet_den_user(data["email"], data["password"]) # schreibweise ggfs ["email"] - kompletter user wird returnt - spezielle data wird gecheckt
        if user: #wird nur returnt, wenn passwort korrekt
            if user.is_active:
                return {'username': user.username, 'email': user.email, 'password': user.password} # in der view, falls ma das brauchen - in der view wird der serializer aufgerufen
        raise serializers.ValidationError("Invalid login data")
    