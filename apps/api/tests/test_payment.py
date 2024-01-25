from django.test import TestCase
from rest_framework.test import APIClient
from apps.advertisement.models import Advertisement, Category
from django.contrib.auth import get_user_model
User = get_user_model()



class UserPayments(TestCase):
    def setUp(self) -> None:
        # self.adv = Ad
        return super().setUp()
    
    def test_create_payment(self):
        pass
        # payment/zarinpal/create-transaction/<int:adv_id>/


