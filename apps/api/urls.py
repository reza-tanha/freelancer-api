from django.urls import include, path
from apps.api.views import *
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from apps.payment.views import ZarinpalCreateTransaction, ZarinpalVerifyTransaction



app_name = 'api'

router = routers.SimpleRouter()
router.register('auth/register', UserRegister, basename='user-register')
router.register('advertisement', AdvertisementViewSet, basename='Advertisement')
router.register('user/advertisement', UserAdvertisementViewSet, basename='user-Advertisement')
router.register('user/payments', UserPaymentViewSet, basename='user-payment')

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('payment/zarinpal/create-transaction/<int:adv_id>/', ZarinpalCreateTransaction.as_view(), name="payment-advertisement-create"),
    path('payment/zarinpal/verify-transaction/', ZarinpalVerifyTransaction.as_view(), name="payment-advertisement-verify"),
] 

urlpatterns += router.urls
