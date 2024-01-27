from django.test import TestCase
from rest_framework.test import APIClient
from apps.advertisement.models import Advertisement, Category
from apps.payment.models import Payment
from django.contrib.auth import get_user_model
User = get_user_model()



class UserPayments(TestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(
            name="test_cat",slug="test_cat",price=2000,
            coin=10,description="hi this is test",
            limit_char=500,is_active=True,position=1
        )
        self.user = User.objects.create_user(
            email="root@email.com",
            username="root",
            password="root",
            phone="09390909090"
        )
        self.adv = Advertisement.objects.create(
            user=self.user,category=self.category,
            text="this is test",contuct="haji"
        )

        self.payment = Payment.objects.create(
            user=self.user,
            amount=20000,
            is_paid=True,
            transaction_id="A00000000000000000000000000499920294",
            advertisement=self.adv
        )
        self.cli = APIClient()
        return super().setUp()
    
    def test_create_payment(self):
        self.cli.login(username="root", password="root")
        response = self.cli.get(f'/api/payment/zarinpal/create-transaction/{self.adv.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('StartPay', response.url.split('/'))

    def test_payments_list(self):
        self.cli.login(username="root", password="root")
        response = self.cli.get(f'/api/user/payments/')
        self.assertIsNone(response.json().get('next'))
        self.assertEqual(response.json().get('count'), 1)
