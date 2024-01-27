from rest_framework.serializers import ModelSerializer
from apps.advertisement.models import Advertisement
from django.contrib.auth import get_user_model
from apps.advertisement.models import Advertisement
from apps.payment.models import Payment


class PaymentUserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'username',]

class PaymentUserAdvertisementSerializer(ModelSerializer):            
    class Meta:
        model = Advertisement
        fields = '__all__'


class UserPaymentSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'request' in self.context and self.context['request'].method == 'GET':
            self.fields['user'] = PaymentUserSerializer()
            self.fields['advertisement'] = PaymentUserAdvertisementSerializer()
    
    class Meta:
        model = Payment
        fields = ['id', 'user', 'created', 'is_paid', 'getway', 'transaction_id', 'advertisement']
