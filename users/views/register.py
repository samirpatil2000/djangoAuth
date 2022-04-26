from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from users.serializers import (
    AccountSerializer,
)
from users.models import User as Account
from users.models import OtpVerify
from django.http import QueryDict
from utils.respones import EdueResponse

class RegistrationAPIView(APIView):

    def get_object(self, user):
        try:
            return Account.objects.get(email=user)
        except Account.DoesNotExist:
            raise Http404

    def create_email(self, phone: str):
        return str(phone) + "@phoneuser.edue.app"

    def get(self, request):
        try:
            if not request.user.is_authenticated:
                result = {'status': status.HTTP_403_FORBIDDEN, "message": "Not Authenticated!", "data": {}}
                return EdueResponse(status=result.get("status"), message=result.get("message"), data=result.get("data"))
            account = self.get_object(request.user)
            serializers = AccountSerializer(account)
            result = {'status': status.HTTP_200_OK, "message": "successfully register", "data": serializers.data}
        except Exception as e:
            result = {'status': status.HTTP_400_BAD_REQUEST, "message": str(e), "data":{}}
        return EdueResponse.set_response(result)

    def post(self, request, *args, **kwargs):
        try:
            try:
                phone_token = OtpVerify().decode_token(request.data.get('phone_token'))
                email_token = {'email': self.create_email(phone_token.get('phone'))}
                if request.data.get('email_token'):
                    email_token = OtpVerify().decode_token(request.data.get('email_token'))
                if isinstance(request.data, QueryDict):  # optional
                    request.data._mutable = True
                request.data.update({
                    'email': email_token.get('email'),
                    'phone': phone_token.get('phone')
                })
                print(request.data)
                account_serializer = AccountSerializer(data=request.data)
            except Exception as e:
                result = {'status':status.HTTP_400_BAD_REQUEST, "message": str(e)}
                return EdueResponse.set_response(result)

            if account_serializer.is_valid():
                account = account_serializer.save()
                result = {
                    'status': status.HTTP_201_CREATED,
                    'message': "successfully register",
                    'data': {
                        "email": account.email,
                        "phone_number": str(account.phone)
                    }
                }
            else:
                result = {'status': status.HTTP_400_BAD_REQUEST, "message": str(account_serializer.error_messages)}
        except Exception as e:
            result = {'status': status.HTTP_400_BAD_REQUEST, "message": str(e)}
        return EdueResponse.set_response(result)
