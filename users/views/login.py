from django.http import Http404
from rest_framework import status
from users.models import User as Account
from rest_framework_simplejwt.views import TokenObtainPairView

from utils.respones import EdueResponse


class LoginAPIView(TokenObtainPairView):

    def get_user_object(self, user):
        try:
            return Account.objects.get(email=user)
        except Account.DoesNotExist:
            raise Http404

    def post(self, request, *args, **kwargs):
        tokens_ = super(TokenObtainPairView, self).post(request, *args, **kwargs)
        result = {'status': status.HTTP_200_OK, 'message': "successfully login", 'data': tokens_.data}
        return EdueResponse.set_response(result)

