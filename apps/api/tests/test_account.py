from email import header
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
User = get_user_model()



class UserRegisteTestCase(TestCase):
    def setUp(self) -> None:
        self.data = {
            "email": "reza@email.com",
            "username": "reza",
            "password": "reza1234",
            "password2": "reza1234",
            "phone": "9030303030"
        }
        return super().setUp()
    
    
    def test_register(self):
        self.cli = APIClient()
        response = self.client.post('/api/auth/register/', data=self.data, format='json')
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(response.status_code, 201)

    def test_token(self):
        self.data.pop("password2")
        User.objects.create_user(
            **self.data
        )
        self.data.pop('phone')
        self.data.pop('email')
        response = self.client.post('/api/auth/token/', data=self.data, format='json')
        self.assertIn('refresh', response.json())
        self.assertIn('access', response.json())
        self.assertEqual(response.status_code, 200)
    
    def test_refresh_token(self):
        self.data.pop("password2")
        User.objects.create_user(
            **self.data
        )
        self.data.pop('phone')
        self.data.pop('email')
        response = self.client.post('/api/auth/token/', data=self.data, format='json')
        refresh = response.json().get("refresh")
        response = self.client.post('/api/auth/token/refresh/', data={'refresh': refresh}, format='json')
        self.assertIn('access', response.json())
        self.assertEqual(response.status_code, 200)


