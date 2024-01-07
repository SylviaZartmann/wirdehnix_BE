from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer): # es wird ein Modellobjekt erstellt bzw. aktualisiert, deswegen ModelSerializer
    conf_password = serializers.CharField(write_only=True) # wird temporär angelegt, für die Registrierung ist auch ohne customUser da, weil nicht dauerhaft in Datenbank
    
    class Meta: 
        model = get_user_model()   
        fields = ('username', 'email', 'password', 'conf_password')
    
    # mit value ist die Liste in fields gemeint - alle werte aus der Liste sind in "value" gespeichert und werden nachfolgend einzeln herausgelesen    
    def val_password(self, value):    
        password = value.get('password')   
        conf_password = value.get('conf_password')   
        
        if password != conf_password:
            raise serializers.ValidationError('No matching passwords!')
        
        else:
            try: 
                validate_password(password) # Django built in Funktion, überprüft, ob das Passwort den Sicherheitsrichtlinien entspricht
            except ValidationError: # Hier wird die Ausnahme abgefangen, falls das Passwort nicht den Anforderungen entspricht
                raise serializers.ValidationError('Password insecure!') # Wenn ValidationError, wird entsprechende Fehlermeldung über Serialisierer zurückgegeben. bedeutet, das Passwort nicht sicher
            
        return value # Wenn Passwort den Anforderungen entspricht, wird das ursprüngliche Passwort zurückgegeben.
        
      
    def val_email(self, value):      
        email = value.get('email')      
        
        try:
            validate_email(email) # Django built in Funktion, überprüft, ob valide Email Addresse
        except ValidationError: 
            raise serializers.ValidationsError('Email address invalid!')
        return value
        

    def create(self, valid_data):
        del valid_data["conf_password"]
        new_user = get_user_model().objects.create_user(**valid_data)
        new_user.is_active = False
        new_user.save()
        confirmation_token = default_token_generator.make_token(new_user)
        uid = urlsafe_base64_encode(force_bytes(new_user.pk)) # um eine URL-sichere Codierung der Benutzer-ID (Primary Key) zu erstellen

        return {"user": new_user, "uid": uid, "token": confirmation_token}

        
class ConfirmEmailSerializer(serializers.Serializer): # gibt dir mehr Flexibilität, ermöglicht es, benutzerdefinierte Validierungslogik ohne die automatische Modellerstellungsfunktionalität bereitzustellen       
        token = serializers.CharField() # vorübergehend ein Feld erstellen, was es danach so nicht mehr gibt
        
        def val_token(self, value):
            
            for user in get_user_model().objects.filter(is_active=False): # in vorheriger Funktion eingefügt
                if default_token_generator.check_token(user, value): # wir checken in den Benutzern, ob das übergebene Token mit einem vorhandenen Token übereinstimmt
                    user.is_active = True # trifft es einen Token, wird is_active auf True gesetzt
                    user.save() # die Änderungen werden gespeichert
                    return value # geben alles zurück
            
            raise serializers.ValidationError("Provided token invalid!") # wenn kein passender Benutzer gefunden wird, gibts nen Fehler
        
        
        
        
        
# class LoginSerializer():
    
    
    
# class LogoutSerializer():
    
    
    
#validation of action and data

# registration - validation of passwords, 
# or is non existing and needs to be created
# password and confirmed password should match
# validate if password is secure
# validation of email address

# new user gets token via email to register
# validate token - and new user create or active

# login with email and password
# email belongs to registered user
# email and password geo together
# give user token - user keeps old token? - nä, da war was
# if its a correct password for existing user

# do we want to change passowrds ?!
# validate email and send new token or activation link in email with token
# overwrite old password with new confirmed password