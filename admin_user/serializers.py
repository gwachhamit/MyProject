from rest_framework import serializers, viewsets 
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group

import django.contrib.auth.password_validation as django_pw_validators

class UserGroupSerializer(serializers. HyperlinkedModelSerializer): 
    class Meta:        
        model = Group        
        fields = (
            'pk', 
            'name'
        )      
        read_only_fields = ('pk','name')

class UserSerializer(serializers. HyperlinkedModelSerializer): 
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(write_only=True,required=False)
    groups = UserGroupSerializer(many=True)
    class Meta:        
        model = User        
        fields = (
            'pk', 
            'first_name', 
            'last_name', 
            'username', 
            'email',
            'password',
            'is_active',
            'is_staff',
            'last_login',
            'date_joined',
            'groups'
        )      
        read_only_fields = ('pk',)

    def validate(self, data):
        """
        Validate passwords by utilizing Django's built in validators
        """
        user = User(**data)
        errors = dict()
        if data.get('password'):
            try:
                django_pw_validators.validate_password(password=data.get('password'), user=user)
            except ValidationError as e:
                errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        """
        group_data = validated_data.pop('groups')
        user = User.objects.create(**validated_data)
        for group in group_data:
            groupObj = Group.objects.get(name=group['name'])
            user.groups.add(groupObj)
        return user

    # def update(self, instance, validated_data):
    #     group_data = validated_data.pop('groups')
    #     instance.first_name = validated_data.get("name",instance.first_name)
    #     instance.last_name = validated_data.get("name",instance.last_name)
    #     instance.username = validated_data.get("name",instance.username)
    #     instance.email = validated_data.get("name",instance.email)
    #     instance.is_staff = validated_data.get("name",instance.is_staff)
    #     instance.save()
    #     #remove all previous groups
    #     for group in instance.groups.all():
    #         groupObj = Group.objects.get(name=group.name)
    #         instance.groups.remove(groupObj)
    #     #add new provided groups
    #     for group in group_data:
    #         groupObj = Group.objects.get(name=group['name'])
    #         instance.groups.add(groupObj)
    #     return instance
