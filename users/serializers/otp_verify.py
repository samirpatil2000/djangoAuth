from rest_framework import serializers


VERIFICATION_MODE =(
    ("0", "PHONE"),
    ("1", "EMAIL")
)


class OtpVerificationSerializer(serializers.Serializer):
    # we can improve this by checking valid phone number
    mode = serializers.ChoiceField(
                    choices = VERIFICATION_MODE)
    phone_number = serializers.CharField()
    email = serializers.EmailField()