# data_manager/urls.py
from django.urls import path
from .views import (
    CategoryListCreateView, CategoryDetailView,
    DeviceListCreateView, DeviceDetailView,
    NodeListCreateView, NodeDetailView,
    EdgeListCreateView, EdgeDetailView,
    FlowListCreateView, FlowDetailView
)

urlpatterns = [
    path('api/categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('api/categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    path('api/devices/', DeviceListCreateView.as_view(), name='device-list'),
    path('api/devices/<int:pk>/', DeviceDetailView.as_view(), name='device-detail'),

    path('api/nodes/', NodeListCreateView.as_view(), name='node-list'),
    path('api/nodes/<int:pk>/', NodeDetailView.as_view(), name='node-detail'),

    path('api/edges/', EdgeListCreateView.as_view(), name='edge-list'),
    path('api/edges/<int:pk>/', EdgeDetailView.as_view(), name='edge-detail'),

    path('api/flows/', FlowListCreateView.as_view(), name='flow-list'),
    path('api/flows/<int:pk>/', FlowDetailView.as_view(), name='flow-detail'),
]
