from rest_framework import serializers
from django.contrib.auth import authenticate
from helpers.serializers_mixins import CustomModelSerializer
from .models import User
import pyotp

class UserSerializer(CustomModelSerializer):
    class Meta:
        model = User
        fields = (
            "uuid",
            "name",
            "email",
            "enable_two_factor_authentication",
        )

class UserAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label="email", write_only=True, required=True)
    password = serializers.CharField(label="Password", style={"input_type": "password"}, trim_whitespace=False, write_only=True, required=True)
    token = serializers.CharField(label="Token", read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(request=self.context.get("request"), email=email, password=password)
            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class TwoFactorAuthTokenSerializer(serializers.Serializer):
    user = serializers.CharField(label="User", write_only=True, required=True)
    otp = serializers.CharField(label="OTP", write_only=True, required=True)

    def validate(self, attrs):
        user_uuid = attrs.get("user")
        otp = attrs.get("otp")
        if not user_uuid:
            raise serializers.ValidationError('Login session expired. Please try again.', code='expired')

        user = User.objects.get(uuid=user_uuid)
        # This is where we confirm the validity of the OTP with PyOTP
        totp = pyotp.TOTP(user.two_fa_identifier)
        token_valid = totp.verify(otp, valid_window=1)
        if not token_valid:
            raise serializers.ValidationError('Invalid MFA token. Please try again.', code='invalid-token')
        attrs["user"] = user
        return attrs
