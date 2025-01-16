from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import models
from calyvim.tasks import file_archive

def get_file_fields(instance):
    return [
        field for field in instance._meta.fields if isinstance(field, models.FileField)
    ]

@receiver(post_delete)
def handle_file_operations_on_delete(sender, instance, **kwargs):
    for field in get_file_fields(instance):
        file_instance = getattr(instance, field.name)
        if file_instance:
            file_archive.delay(file_instance.name)