# Generated by Django 5.1 on 2024-09-22 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("taskite", "0009_rename_accepted_at_workspaceinvite_confirmed_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="workspaceinvite",
            name="invitation_id",
            field=models.CharField(blank=True, max_length=64, null=True, unique=True),
        ),
    ]