# Generated by Django 5.1 on 2024-11-11 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("taskite", "0047_task_is_archived"),
    ]

    operations = [
        migrations.AddField(
            model_name="board",
            name="logo",
            field=models.ImageField(blank=True, null=True, upload_to="boards/logos/"),
        ),
    ]
