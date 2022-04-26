from rest_framework import serializers
from users.models import User as Account


class AccountSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input': 'password'}, write_only=True)
    email_token = serializers.CharField(required=False, write_only=True)
    phone_token = serializers.CharField(required=True, write_only=True)


    class Meta:
        model = Account
        fields = ['email_token', 'email', 'first_name', 'last_name', 'phone', 'phone_token', 'password', 'password2']
        extra_kwargs = {
            'password' : {'write_only': True},
            'email_token' : {'write_only': True},
            'phone_token' : {'write_only': True},
        }

    def save(self):
        account = Account(
                    email=self.validated_data['email'], phone=self.validated_data['phone'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2 :
            raise serializers.ValidationError({'password': 'Password mismatch'})

        account.set_password(password)
        account.save()
        return account

class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


