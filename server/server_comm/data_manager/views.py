from django_filters.rest_framework import (
    DjangoFilterBackend,
    FilterSet,
    NumberFilter,
)
from rest_framework import generics

from .models import Category, Device, Edge, Flow, Node
from .serializers import (
    CategorySerializer,
    DeviceSerializer,
    EdgeSerializer,
    FlowSerializer,
    NodeSerializer,
)


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DeviceFilter(FilterSet):
    category_id = NumberFilter(field_name='category__id', lookup_expr='exact')

    class Meta:
        model = Device
        fields = ['category_id']


class DeviceListCreateView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DeviceFilter


class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class NodeListCreateView(generics.ListCreateAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer


class NodeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer


class EdgeListCreateView(generics.ListCreateAPIView):
    queryset = Edge.objects.all()
    serializer_class = EdgeSerializer


class EdgeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Edge.objects.all()
    serializer_class = EdgeSerializer


class FlowListCreateView(generics.ListCreateAPIView):
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer


class FlowDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer
