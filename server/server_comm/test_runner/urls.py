from django.urls import path

from .views import RunTestFlow

urlpatterns = [
    path('run/<int:flow_id>/', RunTestFlow.as_view(), name='run-test-flow'),
    path('run/', RunTestFlow.as_view(), name='run-all-test-flows'),
]
