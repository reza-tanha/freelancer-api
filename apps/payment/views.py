import json
import requests
from django.shortcuts import redirect
from rest_framework.views import APIView
from apps.payment.models import Payment
from apps.advertisement.models import Advertisement
from django.conf import settings
from rest_framework.response import Response


class ZarinpalMetaData:
    zarinpal_merchant = settings.ZARINPAL_MERCHANT
    zarinpal_api_request = "https://api.zarinpal.com/pg/v4/payment/request.json"
    zarinpal_api_verify = "https://api.zarinpal.com/pg/v4/payment/verify.json"
    zarinpal_api_startpay = "https://www.zarinpal.com/pg/StartPay/{authority}"
    zarinpal_callback = settings.BASE_SITE_URL + "/api/payment/zarinpal/verify-transaction/"
    zarinpal_headers = {
        "accept": "application/json",
        "content-type": "application/json",
    }

class ZarinpalCreateTransaction(APIView, ZarinpalMetaData):

    def get(self, request, adv_id):
        self.adv = Advertisement.objects.filter(id=adv_id).first()
        if not self.adv:
            return
        
        pay_ = self.create_payment()
        serialized_data = self.serialize_send_data()
        try:
            response = self.send_information(data=serialized_data)        
            authority = response["data"]["authority"]
            pay_.transaction_id=authority
            pay_.save()
            if not response["errors"]:
                return redirect(self.zarinpal_api_startpay.format(authority=authority))
            else:
                return Response(f"payment error: {response['errors']['message']}", status=400)
        except:
            return Response(f"payment error: {response['errors']['message']}", status=400)


    def serialize_send_data(self) -> dict:
        """Serialize the data to create the new zarinpal transaction."""
        zarinpal_send_data = {
            "merchant_id": self.zarinpal_merchant,
            "description": "description",
            "amount": self.adv.category.price,
            "callback_url": self.zarinpal_callback.format(),
            "metadata": {"mobile": self.adv.user.phone, "email": self.adv.user.email},
        }
        return zarinpal_send_data
    
    def create_payment(self):
        return Payment.objects.create(
            user=self.adv.user,
            amount=self.adv.category.price,
            advertisement=self.adv
        )

    def send_information(self, data: dict) -> dict:
        """Send ``zarinpal`` information and return the response."""
        data = json.dumps(data)
        response = requests.post(
            url=self.zarinpal_api_request, data=data, headers=self.zarinpal_headers
        ).json()
        return response

class ZarinpalVerifyTransaction(APIView, ZarinpalMetaData):

    def get(self , request):
        status = request.GET.get("Status").lower()
        self.authority = request.GET.get("Authority")

        if status == "ok":
            self.pay = Payment.objects.filter(transaction_id=self.authority).first()
            response = self.prepare_and_send_verify_data(self.pay.amount)
            context_data = self.handel_verify_response(response, self.pay)

            if context_data.get("code") == 100:
                self.pay.is_paid = True
                self.pay.save()
                self.pay.advertisement.status = "wait_for_publish"
                self.pay.advertisement.save()                
                # zarin_logger.log_success_zarinpal_transaction(pay.payer.user_id, pay.amount)
                return redirect(settings.ZARINPAL_REDIRECT_PATH_AFTER_PAYMENT)
        else:
            context_data = {
                "user_id": self.pay.user.id, "authority": self.authority,
                "message": "تراکنش با خطا مواجه شده است"
            }
        return Response(context_data, status=400)

    def prepare_and_send_verify_data(self, amount: int):
        data = {
            "merchant_id": self.zarinpal_merchant,
            "amount": amount,
            "authority": self.authority
        }
        response = requests.post(
            url=self.zarinpal_api_verify,
            data=json.dumps(data),
            headers=self.zarinpal_headers
        ).json()
        return response

    def handel_verify_response(self, response: dict, payment: Payment):
        if response.get("errors"):
            return {
                "message": response["errors"]["message"],
                "authority": self.authority,
                "user_id": payment.user.id,
                "code": response["errors"]["code"]
            }
        else:
            status_code = response["data"]["code"]
            if status_code == 100:
                return {
                    "authority": self.authority,
                    "price": payment.amount,
                    "user id": payment.user.id,
                    "card_pan": response["data"]["card_pan"],
                    "fee": response["data"]["fee"],
                    "user_id":  payment.user.id,
                    "code": 100
                }
            elif status_code == 101:
                return {
                    "message": "تراکنش قبلا وریفای شده است.",
                    "authority": self.authority,
                    "user_id":  payment.user.id,
                    "code": 101
                }
            else:
                return {
                    "message": response["data"]["message"],
                    "authority": self.authority,
                    "user_id":  payment.user.id,
                    "code": status_code
                }
            