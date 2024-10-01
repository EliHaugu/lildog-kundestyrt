from django.db import models

VALID_CONNECTION_TYPES = ["wifi", "bluetooth", "ethernet"]


class Category(models.Model):
    category_name = models.CharField(max_length=255)
    connection_type = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if self.connection_type not in VALID_CONNECTION_TYPES:
            raise ValueError(
                f"Invalid connection type: {self.connection_type}. Must be one of {VALID_CONNECTION_TYPES}."
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name


class Device(models.Model):
    device_id = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.device_id


class Node(models.Model):
    label = models.CharField(max_length=255)
    expected_response = models.CharField(max_length=255)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    function = models.TextField()
    x_pos = models.IntegerField()
    y_pos = models.IntegerField()

    def __str__(self):
        return self.label


class Edge(models.Model):
    source = models.ForeignKey(
        Node, related_name="source_edges", on_delete=models.CASCADE
    )
    target = models.ForeignKey(
        Node, related_name="target_edges", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Edge from {self.source} to {self.target}"


class Flow(models.Model):
    name = models.CharField(max_length=255)
    nodes = models.ManyToManyField(Node)
    edges = models.ManyToManyField(Edge)

    def __str__(self):
        return self.name
