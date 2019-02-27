from rest_framework import serializers, viewsets 
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from customer_user.models import Profile

import django.contrib.auth.password_validation as django_pw_validators

from rest_auth.serializers import UserDetailsSerializer
from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.utils.translation import ugettext_lazy as _
from allauth.utils import (email_address_exists,
                               get_username_max_length)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ( 'user','height','current_weight','target_weight','target_date','workout_time','gender','street',
            'city','state','country')
        read_only_fields = ('user',)

class RegisterCustomerSerializer(serializers. Serializer):  
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    profile = ProfileSerializer(required=False)
    
    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data
    
    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }

    def save_profile(self, user):
        profile_data = self.validated_data.get('profile')
        Profile.objects.update_or_create(user=user,**profile_data)
    
    def set_group(self, user):
        users_group = Group.objects.get(name='customer')
        user.groups.add(users_group)
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.save_profile(user)
        self.set_group(user)
        setup_user_email(request, user, [])
        return user

class UserSerializer(serializers.ModelSerializer):  
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    profile = ProfileSerializer(required=True)
    
    class Meta:
        model = User
        fields = ('pk','username','email','first_name','last_name','profile')

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        """
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user,**profile_data)
        return user

    def update(self, instance, validated_data):
        """
        Overriding the default update method of the Model serializer.
        """
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        if(instance.is_staff == 0):
            profile_data = validated_data.pop('profile')
            # Unless the application properly enforces that this field is
            # always set, the follow could raise a `DoesNotExist`, which
            # would need to be handled.
            profile = instance.profile
            profile.height = profile_data.get('height', profile.height)
            profile.current_weight = profile_data.get('current_weight', profile.current_weight)
            profile.target_weight = profile_data.get('target_weight', profile.target_weight)
            profile.target_date = profile_data.get('target_date', profile.target_date)
            profile.workout_time = profile_data.get('workout_time', profile.workout_time)
            profile.gender = profile_data.get('gender', profile.gender)
            profile.street = profile_data.get('street', profile.street)
            profile.city = profile_data.get('city', profile.city)
            profile.state = profile_data.get('state', profile.state)
            profile.country = profile_data.get('country', profile.country)
            profile.save()

        return instance
