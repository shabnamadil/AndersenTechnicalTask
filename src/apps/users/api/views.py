from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .serializers import RegisterSerializer
from django.conf import settings
from utils.views.refresh_cookie import set_refresh_cookie


User = get_user_model()


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        access_token = response.data.get("access")
        refresh_token = response.data.get("refresh")

        news_response = Response({"access": access_token}, status=status.HTTP_200_OK)
        set_refresh_cookie(news_response, refresh_token)

        return Response({"detail": "Token was given successfully"}, status=status.HTTP_200_OK)


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token not found in cookie"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data={"refresh": refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response(
                {"detail": "Invalid or expired refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        access_token = serializer.validated_data.get("access")
        new_refresh_token = serializer.validated_data.get("refresh")

        new_response = Response({"access": access_token}, status=status.HTTP_200_OK)
        set_refresh_cookie(new_response, new_refresh_token)

        return Response({"detail": "Token was renewed successfully"}, status=status.HTTP_200_OK)
    

class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token not found in cookie"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response(
                {"detail": "Invalid or expired refresh token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = Response({"detail": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        response.delete_cookie("refresh_token", path="/api/token/refresh/")
        return response
    

class LogoutAllDevicesAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)
        return Response(status=status.HTTP_205_RESET_CONTENT)