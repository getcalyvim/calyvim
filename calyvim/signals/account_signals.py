from django.db.models.signals import post_save
from django.dispatch import receiver
from calyvim.models import (
    WorkspaceMembership,
    Workspace,
    User,
)


# @receiver(post_save, sender=User)
# def assign_membership_via_workspace_domain(sender, instance, created, **kwargs):
#     if created and not instance.is_generic_email:
#         # Extract domain from email
#         domain = instance.email.split("@")[1]
#         workspace = Workspace.objects.filter(auto_assign_domain=domain).first()
#         if workspace and workspace.auto_assign_membership:
#             WorkspaceMembership.objects.create(
#                 user=instance,
#                 workspace=workspace,
#                 role=WorkspaceMembership.Role.COLLABORATOR,
#             )
