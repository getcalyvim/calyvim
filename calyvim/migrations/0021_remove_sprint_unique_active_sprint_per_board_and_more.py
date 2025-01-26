# Generated by Django 5.1 on 2025-01-26 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calyvim", "0020_prefill_workspace_code"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="sprint",
            name="unique_active_sprint_per_board",
        ),
        migrations.AddField(
            model_name="sprint",
            name="goals",
            field=models.TextField(blank=True, null=True),
        ),
    ]
