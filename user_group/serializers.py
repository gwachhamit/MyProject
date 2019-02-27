from rest_framework import serializers, viewsets 
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group, Permission

class PermissionSerializer(serializers. HyperlinkedModelSerializer): 
    class Meta:        
        model = Permission        
        fields = (
            'pk', 
            'codename',
            'name'
        )      
        read_only_fields = ('pk','name')

class UserGroupSerializer(serializers. HyperlinkedModelSerializer): 
    permissions = PermissionSerializer(many=True)
    class Meta:        
        model = Group        
        fields = (
            'pk', 
            'name',
            'permissions'
        )      
        read_only_fields = ('pk',)

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        """
        permission_data = validated_data.pop('permissions')
        group = Group.objects.create(**validated_data)
        for permission in permission_data:
            permissionNow = Permission.objects.get(codename=permission['codename'])
            group.permissions.add(permissionNow)
        return group

    def update(self, instance, validated_data):
        permission_data = validated_data.pop('permissions')
        instance.name = validated_data.get("name",instance.name)
        instance.save()
        #remove all previous permissions
        for permission in instance.permissions.all():
            permissionNow = Permission.objects.get(codename=permission.codename)
            instance.permissions.remove(permissionNow)
        #add new provided permissions
        for permission in permission_data:
            permissionNow = Permission.objects.get(codename=permission['codename'])
            instance.permissions.add(permissionNow)
        return instance
