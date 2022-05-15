from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status, permissions
from .serializers import UserAuthTokenSerializer, UserSerializer, TwoFactorAuthTokenSerializer
from helpers.api_mixins import CustomAPIMixin
import pyotp

class ObtainAuthTokenView(CustomAPIMixin, APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        serializer = UserAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if user.enable_two_factor_authentication:
            return self.api_success_response({
                "message": "Please enter your 2FA code.",
                "redirect_to_tfa": True,
                "user": user.uuid
            })
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        user_serializer = UserSerializer(user)
        return self.api_success_response(
            {
                "message": "Success",
                "token": token.key,
                "user": user_serializer.data,
                "redirect_to_tfa": False
            }
        )

class TwoFactorAuthTokenView(CustomAPIMixin, APIView):
    permission_classes = [permissions.AllowAny, ]
    def post(self, request):
        user = request.user
        serializer = TwoFactorAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        user_serializer = UserSerializer(user)
        return self.api_success_response(
            {
                "message": "Success",
                "token": token.key,
                "user": user_serializer.data,
                "redirect_to_tfa": False
            }
        )

class EnableTwoFactorAuthenticationAPIView(CustomAPIMixin, APIView):

    def post(self, request):
        user = request.user
        url = pyotp.TOTP(user.two_fa_identifier).provisioning_uri(user.email, issuer_name="Sparrow SMS")
        if user.enable_two_factor_authentication:
            return self.api_error_response({"message": "Two factor authentication is already enabled.", "url": url}, status.HTTP_200_OK)
        user.enable_two_factor_authentication = True
        user.save()
        return self.api_success_response(
            {
                "message": "Two factor authentication is enabled.",
                "url": url,
            }
        )