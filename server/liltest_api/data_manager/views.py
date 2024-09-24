from rest_framework import generics
from .models import Item
from .serializers import ItemSerializer

# List all items or create a new one
class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

# Retrieve, update, or delete an item by ID
class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
