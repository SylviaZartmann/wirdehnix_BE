from django.core.mail import send_mail

def send_activationmail_to_user(new_user, confirmation_token, uid):
    confirmation_link = f"https://wirdehnix.sylviazartmann.de/confirm-registration/?uid={uid}&token={confirmation_token}" # Bestätigungslink erstellen

    message = f"Hi {new_user.username},\n\nPlease click the following link to activate your account:\n{confirmation_link}"
        
    send_mail(
        "Account Activation",
        message,
        "noreply@wirdehnix.com",
        [new_user.email],
        fail_silently=False,
    )
    
def gibbet_den_user(email, password):
    try: 
        user = user.objects.get(email=email) # wir holen uns den user anhand der vorhandenen email
        if user.check_password(password): # wir überprüfen das passwort mit dem vorhandenen passwort
            return user # wir geben den user als solchen zurück, weil passt
        # warum auch immer gehts hier in die view ?! 
    except user.DoesNotExist:
        return None