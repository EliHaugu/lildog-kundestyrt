# Generated by Django 5.1.1 on 2024-10-21 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_manager', '0004_remove_node_expected_response_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='connection_ids',
            field=models.JSONField(default=dict),
        ),
    ]
