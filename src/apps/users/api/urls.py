from django.urls import path

from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    LogoutAPIView,
    RegisterAPIView,
    LogoutAllDevicesAPIView
)

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path(
        "token/",
        CustomTokenObtainPairView.as_view(),
        name="custom_token_obtain_pair",
    ),
    path(
        "token/refresh/",
        CustomTokenRefreshView.as_view(),
        name="custom_token_refresh",
    ),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("logout_all/", LogoutAllDevicesAPIView.as_view(), name="logout_all")
]
