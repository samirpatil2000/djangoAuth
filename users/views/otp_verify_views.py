from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.models import OtpVerify


def send_otp_to_user(phone_number=None, email=None):
    if phone_number:
        generated_otp = OtpVerify().generate_phone_otp(phone_number)
        # send_opt_function with third party integration eg twillio
        print(generated_otp, phone_number)
    elif email:
        generated_otp = OtpVerify().generate_email_otp(email)
        # smtp integration
        print(generated_otp, email)
    return


@api_view(['POST'])
def send_otp(request):
    mode = request.data.get('mode')
    if mode == "PHONE":
        phone_number = request.data.get('phone_number')
        send_otp_to_user(phone_number=phone_number)
        result = {'status': 1, 'message': "Otp send successfully to your phone number"}
    elif mode == "EMAIL":
        email = request.data.get('email')
        send_otp_to_user(email=email)
        result = {'status': 1, 'message': "Otp send successfully to your email"}
    else:
        result = {'status': 0, 'message': "Invalid Mode."}
    return Response(result)


@api_view(['POST'])
def verify_otp(request):
    otp = request.data.get('otp')
    mode = request.data.get('mode')
    if mode == "PHONE":
        phone_number = request.data.get('phone_number')
        token = OtpVerify().verify_phone_otp(otp, phone_number)
    elif mode == "EMAIL":
        email = request.data.get('email')
        token = OtpVerify().verify_email_otp(otp, email)
    else:
        return Response({'status': 0, 'message': "Invalid Mode."})

    if not token:
        return Response({'status': 0, 'message': "Invalid Token."})

    return Response({'status': 1, 'message': 'verify', 'data': {'token': str(token)}})


"""
@api_view(['POST'])
def check_validation(request):
    if request.method == 'POST':
        result = {}
        hash_ = request.data.get("hash_")
        if hash_:
            response = OtpVerify().decode_token(hash_)
            result = {'status': 1, 'message': "successful", 'data': response}
        return Response(result)
"""
