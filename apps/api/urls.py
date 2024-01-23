from django.urls import include, path
from apps.api.views import *
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)




app_name = 'api'
urlpatterns = []

router = routers.SimpleRouter()
router.register('auth/register', UserRegister, basename='user-register')
router.register('advertisement', AdvertisementViewSet, basename='Advertisement')
urlpatterns += [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] 

urlpatterns += router.urls
