from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from apps.advertisement.models import Advertisement
from apps.payment.models import Payment
from apps.api.serializers import *
from apps.api.serializer.advertisment import AdvertisementSerializer, UserAdvertisementSerializer
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from apps.api.utils.pageination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend



class UserRegister(ModelViewSet):

    queryset = get_user_model().objects.all()
    serializer_class = UserRegisterSerializer
    http_method_names = ('post', )
    authentication_classes = ()


@method_decorator(cache_page(15), name='dispatch')
class AdvertisementViewSet(ModelViewSet):
    serializer_class = AdvertisementSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ('post', "get", "list")
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('type_adv', 'contuct', 'warning_tag', 'is_expired')

    def get_queryset(self):
        print("Queryset is called!")
        return Advertisement.objects.filter(
            status="publish"
        ).select_related("user", "type_adv").order_by("-id")
    
@method_decorator(cache_page(20), name='dispatch')
class UserAdvertisementViewSet(ModelViewSet):
    serializer_class = UserAdvertisementSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ("put","get", "list")
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('type_adv', 'contuct', 'status', 'warning_tag', 'is_expired')

    def get_queryset(self):
        print("Queryset is called!")
        return Advertisement.objects.filter(
            user=self.request.user
        ).select_related("user", "type_adv").order_by("-id")
    
@method_decorator(cache_page(20), name='dispatch')
class UserPaymentViewSet(ModelViewSet):
    from apps.api.serializer.payment import UserPaymentSerializer
    serializer_class = UserPaymentSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ("get", "list")
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('is_paid', 'getway', 'transaction_id')

    def get_queryset(self):
        print("Queryset is called!")
        return Payment.objects.filter(
            user=self.request.user
        ).select_related("user", "advertisement").order_by("-id")
