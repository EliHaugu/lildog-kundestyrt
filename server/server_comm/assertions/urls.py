from django.urls import path

from . import views

urlpatterns = [
    path(
        'check_assertion/<int:node_id>/',
        views.check_assertion_view,
        name='check_assertion',
    ),
]
