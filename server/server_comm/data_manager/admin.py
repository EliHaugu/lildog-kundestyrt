from django.contrib import admin
from .models import Category, Device, Node, Flow, Edge

admin.site.register(Category)
admin.site.register(Device)
admin.site.register(Node)
admin.site.register(Flow)
admin.site.register(Edge)


