# Generated by Django 5.1 on 2024-11-08 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("taskite", "0046_alter_boardteampermission_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="is_archived",
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]