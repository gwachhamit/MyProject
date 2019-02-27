from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.test import force_authenticate
import json

# Create your tests here.

class TestGroup(APITestCase):
    # Test module for Admin User api

    def setUp(self):
        self.customer = Group.objects.create(name='customer')
        self.new_group = {'name': 'developer','permissions':[]}
        
    def test_get_all_groups(self):
        url = reverse('group-list')
        # get API response
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)   

    def test_get_group(self):
        # get API response
        response = self.client.get(reverse('group-show',kwargs={'pk':self.customer.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_group(self):
        # get API response
        response = self.client.post(
            reverse('group-create'),
            data=json.dumps(self.new_group),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_group(self):
        response = self.client.put(
            reverse('group-update',kwargs={'pk':self.customer.pk}),
            data=json.dumps(self.new_group),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_user(self):
        # get API response
        response = self.client.delete(
            reverse('group-delete',kwargs={'pk':self.customer.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        