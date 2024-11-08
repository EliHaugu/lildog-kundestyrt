from consts import comm_protocol_id_mapping, conn_type_id_mapping
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models


class Category(models.Model):
    WIFI = "wifi"
    BLUETOOTH = "bluetooth"
    LTE = "lte"

    COMMUNICATION_PROTOCOLS_CHOICES = [
        (WIFI, "WiFi"),
        (BLUETOOTH, "Bluetooth"),
        (LTE, "LTE"),
    ]

    ADB = "adb"
    UART = "uart"

    CONNECTION_TYPES_CHOICES = [
        (ADB, "ADB"),
        (UART, "UART"),
    ]

    category_name: models.CharField = models.CharField(max_length=255)
    communication_protocols: ArrayField = ArrayField(
        models.CharField(
            max_length=50,
            choices=COMMUNICATION_PROTOCOLS_CHOICES,
        ),
        size=len(COMMUNICATION_PROTOCOLS_CHOICES),
        default=list,
        blank=True,
    )

    connection_types: ArrayField = ArrayField(
        models.CharField(
            max_length=50,
            choices=CONNECTION_TYPES_CHOICES,
        ),
        default=list,
        blank=True,
    )

    def clean(self):

        if not isinstance(self.communication_protocols, list):
            raise ValidationError("communication_protocols must be a list.")

        invalid_communication_protocols = [
            protocol
            for protocol in self.communication_protocols
            if protocol
            not in dict(self.COMMUNICATION_PROTOCOLS_CHOICES).keys()
        ]
        if invalid_communication_protocols:
            raise ValidationError(
                f"""Invalid communication protocols:
                 {', '.join(invalid_communication_protocols)}.
                 Must be one of {self.COMMUNICATION_PROTOCOLS_CHOICES}."""
            )

        if not isinstance(self.connection_types, list):
            raise ValidationError("connection_types must be a list.")

        invalid_connection_types = [
            conn
            for conn in self.connection_types
            if conn not in dict(self.CONNECTION_TYPES_CHOICES).keys()
        ]
        if invalid_connection_types:
            raise ValidationError(
                f"""Invalid connection types:
                 {', '.join(invalid_communication_protocols)}.
                 Must be one of {self.CONNECTION_TYPES_CHOICES}."""
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
    connection_ids: models.JSONField = models.JSONField(
        default=dict, blank=True, null=True
    )
    communication_ids: models.JSONField = models.JSONField(
        default=dict, blank=True, null=True
    )

    def clean(self):
        for conn_type, conn_id in conn_type_id_mapping.items():
            if (
                conn_type in self.category.connection_types
                and conn_id not in self.category.connection_types
                and not self.connection_ids.get(conn_id)
            ):
                raise ValidationError(
                    f"All {conn_type} devices must have a {conn_id} field."
                )

        invalid_connection_keys = [
            key
            for key in self.connection_ids.keys()
            if key not in conn_type_id_mapping.values()
        ]
        if invalid_connection_keys:
            raise ValidationError(
                f"""Invalid connection_ids keys:
                 {', '.join(invalid_connection_keys)}.
                 Must be one of {list(conn_type_id_mapping.values())}."""
            )

        invalid_communication_keys = [
            key
            for key in self.communication_ids.keys()
            if key not in comm_protocol_id_mapping.values()
        ]
        if invalid_communication_keys:
            raise ValidationError(
                f"""Invalid communication_ids keys:
                 {', '.join(invalid_communication_keys)}.
                 Must be one of {list(comm_protocol_id_mapping.values())}."""
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.device_id


class Node(models.Model):
    ACTION = "Action"
    ASSERT = "Assert"

    NODE_TYPE_CHOICES = [
        (ACTION, "Action"),
        (ASSERT, "Assert"),
    ]

    label: models.CharField = models.CharField(max_length=255)
    node_type: models.CharField = models.CharField(
        max_length=50, choices=NODE_TYPE_CHOICES, default=ACTION
    )
    device: models.ForeignKey = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    function: models.TextField = models.TextField()
    x_pos: models.IntegerField = models.IntegerField(blank=True, null=True)
    y_pos: models.IntegerField = models.IntegerField(blank=True, null=True)

    def clean(self):
        if self.node_type not in dict(self.NODE_TYPE_CHOICES).keys():
            raise ValidationError(
                f"""Invalid node type: {self.node_type}.
                 Must be one of {self.NODE_TYPE_CHOICES}."""
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.label} ({self.node_type})"


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
    nodes: models.ManyToManyField = models.ManyToManyField(Node, blank=True)
    edges: models.ManyToManyField = models.ManyToManyField(Edge, blank=True)

    def __str__(self):
        return self.name
