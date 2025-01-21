# Generated by Django 5.1 on 2025-01-16 19:20

from django.db import migrations
from django.utils.html import strip_tags


def populate_description_raw(apps, schema_editor):
    # Get the Task model dynamically
    Task = apps.get_model("calyvim", "Task")

    # Iterate through all Task objects
    for task in Task.objects.all():
        if task.description:  # Check if description is not None or empty
            task.description_raw = strip_tags(task.description)
            task.save(
                update_fields=["description_raw"]
            )  # Save only the 'description_raw' field


class Migration(migrations.Migration):

    dependencies = [
        ("calyvim", "0013_task_description_raw"),
    ]

    operations = [
        migrations.RunPython(
            populate_description_raw, reverse_code=migrations.RunPython.noop
        ),
    ]
