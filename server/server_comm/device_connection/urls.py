from django.urls import path

from .views import SerialDeviceConnectionView

urlpatterns = [
    path(
        "uart/", SerialDeviceConnectionView.as_view(), name="uart-connection"
    ),
]
