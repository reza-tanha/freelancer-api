from rest_framework.serializers import ModelSerializer, ValidationError
from apps.advertisement.models import Advertisement
from django.contrib.auth import get_user_model
from apps.advertisement.models import Advertisement, Category


class ADVTypeAdvSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'price','coin', 'description', 'slug']

class ADVUserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'username',]

class AdvertisementSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'request' in self.context and self.context['request'].method == 'GET':
            self.fields['user'] = ADVUserSerializer()
            self.fields['category'] = ADVTypeAdvSerializer()
            
    class Meta:
        model = Advertisement
        fields = '__all__'
        read_only_fields = ('status', 'warning_tag', 'user', 'created', 'is_expired')
        extra_kwargs = {
            'text': {
                "required": True, "allow_null": False
            },
            'contuct': {
                 "required": True, "allow_null": False
            }
        }

    def create(self, validated_data):
        validated_data['user']=self.context.get("request").user
        return super().create(validated_data)
   

class UserAdvertisementSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'request' in self.context and self.context['request'].method == 'GET':
            self.fields['user'] = ADVUserSerializer()
            self.fields['category'] = ADVTypeAdvSerializer()
            
    class Meta:
        model = Advertisement
        fields = '__all__'
        read_only_fields = ('status', 'warning_tag', 'user', 'created')

    def update(self, instance, validated_data):
        if len(validated_data) == 1 and validated_data.get('is_expired') is not None:
            return super().update(instance, validated_data)
        if instance.status == 'publish':
            raise ValidationError("this advertisement is published ! you can't changed")
        return super().update(instance, validated_data)