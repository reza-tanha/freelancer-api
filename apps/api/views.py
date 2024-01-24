from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from apps.advertisement.models import Advertisement
from apps.api.serializers import *
from apps.api.serializer.advertisment import AdvertisementSerializer
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.api.utils.pageination import CustomPagination


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

    def get_queryset(self):
        print("Queryset is called!")
        return Advertisement.objects.filter(
            status="publish"
        ).select_related("user", "type_adv").order_by("-id")
    
@method_decorator(cache_page(1 * 60), name='dispatch')
class UserAdvertisementViewSet(ModelViewSet):
    serializer_class = AdvertisementSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ("put","get", "list")
    pagination_class = CustomPagination

    def get_queryset(self):
        print("Queryset is called!")
        return Advertisement.objects.filter(
            user=self.request.user
        ).select_related("user", "type_adv").order_by("-id")
