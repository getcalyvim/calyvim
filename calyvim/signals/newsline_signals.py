from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from calyvim.models import Newsline, NewslinePermission, WorkspaceMembership

@receiver(post_save, sender=Newsline)
def create_newsline_permission(sender, instance, created, **kwargs):
    if created:
        workspace_membership = WorkspaceMembership.objects.filter(
            user=instance.author, workspace=instance.workspace
        ).first()
        if not workspace_membership:
            raise ObjectDoesNotExist("No membership found for the user")

        NewslinePermission.objects.create(
            newsline=instance,
            user=instance.author,
            workspace_membership=workspace_membership,
        )