# Generated by Django 5.1 on 2025-01-11 14:08

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calyvim", "0009_task_completed_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="documentpermission",
            name="role",
            field=models.CharField(
                choices=[("editor", "Editor"), ("viewer", "Viewer")],
                default="viewer",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="documentteampermission",
            name="role",
            field=models.CharField(
                choices=[("editor", "Editor"), ("viewer", "Viewer")],
                default="viewer",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="content",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.UUIDField(), blank=True, default=list, size=None
            ),
        ),
    ]
