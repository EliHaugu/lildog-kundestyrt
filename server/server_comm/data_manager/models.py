from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models

VALID_CONNECTION_TYPES = ["wifi", "bluetooth", "ethernet"]


class Category(models.Model):
    category_name: models.CharField = models.CharField(max_length=255)
    connection_types: ArrayField = ArrayField(
        models.CharField(
            max_length=50,
            choices=[(conn, conn) for conn in VALID_CONNECTION_TYPES],
        ),
        size=len(VALID_CONNECTION_TYPES),
        default=list,
    )

    def clean(self):
        if not isinstance(self.connection_types, list):
            raise ValidationError("connection_types must be a list.")

        invalid_types = [
            conn
            for conn in self.connection_types
            if conn not in VALID_CONNECTION_TYPES
        ]

        if invalid_types:
            raise ValidationError(
                f"Invalid connection types: {', '.join(invalid_types)}. "
                f"Must be one of {VALID_CONNECTION_TYPES}."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name


class Device(models.Model):
    device_id: models.CharField = models.CharField(max_length=255, unique=True)
    category: models.ForeignKey = models.ForeignKey(
        Category, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.device_id


class Node(models.Model):
    label: models.CharField = models.CharField(max_length=255)
    expected_response: models.CharField = models.CharField(max_length=255)
    device: models.ForeignKey = models.ForeignKey(
        Device, on_delete=models.CASCADE
    )
    function: models.TextField = models.TextField()
    x_pos: models.IntegerField = models.IntegerField()
    y_pos: models.IntegerField = models.IntegerField()

    def __str__(self):
        return self.label


class Edge(models.Model):
    source: models.ForeignKey = models.ForeignKey(
        Node, related_name="source_edges", on_delete=models.CASCADE
    )
    target: models.ForeignKey = models.ForeignKey(
        Node, related_name="target_edges", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Edge from {self.source} to {self.target}"


class Flow(models.Model):
    name: models.CharField = models.CharField(max_length=255)
    nodes: models.ManyToManyField = models.ManyToManyField(Node)
    edges: models.ManyToManyField = models.ManyToManyField(Edge)

    def __str__(self):
        return self.name
