from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from admin_user.serializers import UserSerializer
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.test import force_authenticate
import json

# Create your tests here.

class TestAdminUser(APITestCase):
    # Test module for Admin User api

    def setUp(self):
        self.david = User.objects.create(
            first_name='David', last_name='Guetta', username='dj_david', email='david@gmail.com',password='djDavid123',is_superuser=0
        )
        self.new_user = {
            'first_name': 'Amit',
            'last_name': 'Gwachha',
            'username': 'amitgwachha',
            'email': 'amitgwachha@gmail.com',
            'password': '123456',
            'is_superuser':False
        }
        
    def test_get_all_users(self):
        # get user with username dj_david
        user = User.objects.get(username='dj_david')
        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse('users')
        # get API response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)   

    def test_get_user(self):
        # get user with username dj_david
        user = User.objects.get(username='dj_david')
        client = APIClient()
        client.force_authenticate(user=user)
        # get API response
        response = self.client.get(reverse('user-show',kwargs={'pk':self.david.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_user(self):
        # get user with username dj_david
        user = User.objects.get(username='dj_david')
        client = APIClient()
        client.force_authenticate(user=user)
        # get API response
        response = self.client.post(
            reverse('users'),
            data=json.dumps(self.new_user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_user(self):
        # get API response
        user = User.objects.get(username='dj_david')
        client = APIClient()
        client.force_authenticate(user=user)
        response = self.client.put(
            reverse('user-update',kwargs={'pk':self.david.pk}),
            data=json.dumps(self.new_user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_user(self):
        user = User.objects.get(username='dj_david')
        client = APIClient()
        client.force_authenticate(user=user)
        # get API response
        response = self.client.delete(
            reverse('user-update',kwargs={'pk':self.david.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        