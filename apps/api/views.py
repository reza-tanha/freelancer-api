from rest_framework.viewsets import ModelViewSet
from apps.advertisement.models import Advertisement
from apps.api.serializers import *
from apps.api.serializer.advertisment import AdvertisementSerializer
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_cookie, vary_on_headers


class UserRegister(ModelViewSet):

    queryset = get_user_model().objects.all()
    serializer_class = UserRegisterSerializer
    http_method_names = ('post', )
    authentication_classes = ()


# @method_decorator(cache_page(15), name='dispatch')
class AdvertisementViewSet(ModelViewSet):
    serializer_class = AdvertisementSerializer

    CACHE_KEY_PREFIX = "all_advertisements_cache"

    # @method_decorator(cache_page(10))
    # @method_decorator(cache_page(10, key_prefix=CACHE_KEY_PREFIX))
    @method_decorator(vary_on_cookie)
    def list(self, request, format=None, *args, **kwargs):
    # def list(self, request, *args, **kwargs):
        print("List View is called!")
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        print("Queryset is called!")
        return Advertisement.objects.filter(
            status="publish"
        ).select_related("user", "type_adv")
    
    # @method_decorator(cache_page(10, key_prefix=CACHE_KEY_PREFIX))
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)