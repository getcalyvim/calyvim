# Generated by Django 5.1 on 2025-01-18 03:59

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calyvim", "0016_alter_taskstatelog_changed_by_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="TaskSnapshot",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("date", models.DateField()),
                (
                    "state",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="calyvim.state"
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="snapshots",
                        to="calyvim.task",
                    ),
                ),
            ],
            options={
                "db_table": "task_snapshots",
                "ordering": ["date"],
                "unique_together": {("task", "date")},
            },
        ),
    ]
