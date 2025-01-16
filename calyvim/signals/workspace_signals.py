from django.db.models.signals import post_save
from django.dispatch import receiver
from calyvim.models import Workspace, WorkspaceMembership


@receiver(post_save, sender=Workspace)
def create_default_workspace(sender, instance, created, **kwargs):
    if created:
        WorkspaceMembership.objects.create(
            workspace=instance,
            user=instance.created_by,
            role=WorkspaceMembership.Role.ADMIN,
        )
