from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

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
            validate_email(email) 
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
                validate_password(password)
            except ValidationError: 
                raise serializers.ValidationError('Password insecure!')
            
        return value
        
    def create(self, valid_data):
        del valid_data["conf_password"]
        new_user = get_user_model().objects.create(**valid_data)
        new_user.set_password(valid_data["password"])
        new_user.is_active = False
        new_user.save()
        
        return new_user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True) 
    password = serializers.CharField(write_only=True, required=True)
      
    def validate(self, data):
        user = utils.gibbet_den_user(data["email"], data["password"]) 
        if user: 
            if user.is_active:
                return {'username': user.username, 'email': user.email, 'password': user.password} 
        raise serializers.ValidationError("Invalid login data")
    