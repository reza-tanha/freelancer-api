from rest_framework.viewsets import ModelViewSet
from apps.api.serializers import *



class UserRegister(ModelViewSet):

    queryset = get_user_model().objects.all()
    serializer_class = UserRegisterSerializer
    http_method_names = ('post', )
    authentication_classes = ()

