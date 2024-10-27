from django.urls import path

from .views import (
    AndroidDeviceConnectionView,
    APIConnectionView,
    SerialDeviceConnectionView,
)

urlpatterns = [
    path(
        "serial/",
        SerialDeviceConnectionView.as_view(),
        name="serial-connection",
    ),
    path(
        "android/",
        AndroidDeviceConnectionView.as_view(),
        name="android-connection",
    ),
    path("api/", APIConnectionView.as_view(), name="api-connection"),
]
