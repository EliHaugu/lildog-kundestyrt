from django.urls import path

from .views import (
    AndroidDeviceConnectionView,
    APIConnectionView,
    FlowDeviceConnectionView,
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
    path(
        "connect_flow/",
        FlowDeviceConnectionView.as_view(),
        name="flow-connection",
    ),
]
