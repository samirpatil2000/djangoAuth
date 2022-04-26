from django.urls import path

from rest_framework_simplejwt import views as jwt_views
from users.views import RegistrationAPIView, ChangePasswordView, LoginAPIView
from users.views import otp_verify_views

# def get_tokens_for_user(request):
#     # find the user base in params
#     user = User.objects.first()
#
#     refresh = RefreshToken.for_user(user)
#
#     return Response({
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     })


urlpatterns = [
    path('api/token/refresh/',
         jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('register/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('send-otp/', otp_verify_views.send_otp),
    path('verify-otp/', otp_verify_views.verify_otp),
]
