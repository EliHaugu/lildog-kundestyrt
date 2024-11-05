from django.forms import ValidationError
from django_filters.rest_framework import (
    DjangoFilterBackend,
    FilterSet,
    NumberFilter,
)
from rest_framework import generics
from rest_framework.exceptions import ValidationError as DRFValidationError

from .models import Category, Device, Edge, Flow, Node
from .serializers import (
    CategorySerializer,
    DeviceSerializer,
    EdgeSerializer,
    FlowSerializer,
    NodeSerializer,
)

def handle_validation(view_func):
    def wrapper(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except ValidationError as e:
            raise DRFValidationError(e.messages)
    return wrapper

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @handle_validation
    def perform_create(self, serializer):
        serializer.save()

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

    @handle_validation
    def perform_create(self, serializer):
        serializer.save()

class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    @handle_validation
    def perform_update(self, serializer):
        serializer.save()

class NodeListCreateView(generics.ListCreateAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

    @handle_validation
    def perform_create(self, serializer):
        serializer.save()

class NodeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

    @handle_validation
    def perform_update(self, serializer):
        serializer.save()

class EdgeListCreateView(generics.ListCreateAPIView):
    queryset = Edge.objects.all()
    serializer_class = EdgeSerializer

    @handle_validation
    def perform_create(self, serializer):
        serializer.save()

class EdgeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Edge.objects.all()
    serializer_class = EdgeSerializer

    @handle_validation
    def perform_update(self, serializer):
        serializer.save()

class FlowListCreateView(generics.ListCreateAPIView):
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer

    @handle_validation
    def perform_create(self, serializer):
        serializer.save()

class FlowDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer

    @handle_validation
    def perform_update(self, serializer):
        serializer.save()
