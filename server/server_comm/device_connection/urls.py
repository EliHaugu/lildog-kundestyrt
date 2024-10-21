from django.urls import path

from .views import AndroidDeviceConnectionView, SerialDeviceConnectionView

urlpatterns = [
    path(
        "serial/", SerialDeviceConnectionView.as_view(), name="serial-connection",
    ),
    path(
        "android/", AndroidDeviceConnectionView.as_view(), name="android-connection",
    ),
]
