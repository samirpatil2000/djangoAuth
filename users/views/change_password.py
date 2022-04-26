from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.serializers import (
    ChangePasswordSerializer,
)
from users.models import User as Account

from utils.respones import EdueResponse



class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, user):
        try:
            return Account.objects.get(email=user)
        except Account.DoesNotExist:
            raise Http404

    def patch(self, request, *args, **kwargs):
        try:
            current_account = self.get_object(request.user)
            serializer = ChangePasswordSerializer(data=request.data)
            if serializer.is_valid():
                old_password = serializer.data.get("old_password")
                new_password = serializer.data.get("new_password")
                if not current_account.check_password(old_password):
                    result = {'status': '0', 'message': "Wrong Password!"}
                    return Response(result)
                current_account.set_password(new_password)
                current_account.save()
                result = {'status': status.HTTP_200_OK, 'message': 'password updated successfully'}
            else:
                result = {'status': status.HTTP_400_BAD_REQUEST, 'message': str(serializer.error_messages)}
        except Exception as e:
            result = {'status': status.HTTP_400_BAD_REQUEST, 'message': str(e)}
        return EdueResponse.set_response(result)
