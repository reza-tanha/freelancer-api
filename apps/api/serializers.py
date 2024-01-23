from rest_framework.serializers import ModelSerializer, CharField
from apps.api.utils.validator import UserRegisterValidator
from django.contrib.auth import get_user_model
from apps.advertisement.models import Advertisement



class UserRegisterSerializer(ModelSerializer, UserRegisterValidator):
    password = CharField(write_only=True)
    password2 = CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'username', 'password','password2', 'phone', 'coin']
        write_only_fields = ('password', 'password2')
        read_only_fields = ('id','coin')

    def create(self, validated_data):
        self.password_validateor(validated_data)

        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            phone=validated_data['phone'],
            password=validated_data['password']
        )
        return user