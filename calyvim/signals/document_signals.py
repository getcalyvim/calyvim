from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from calyvim.models import Document, DocumentPermission, WorkspaceMembership, Block


@receiver(post_save, sender=Document)
def create_document_permission(sender, instance, created, **kwargs):
    if created:
        workspace_membership = WorkspaceMembership.objects.filter(
            user=instance.author, workspace=instance.workspace
        ).first()
        if not workspace_membership:
            raise ObjectDoesNotExist("No membership found for the user")

        DocumentPermission.objects.create(
            document=instance,
            user=instance.author,
            workspace_membership=workspace_membership,
            role="editor",
        )


@receiver(post_save, sender=Document)
def create_document_block(sender, instance, created, **kwargs):
    if created:
        block = Block.objects.create(
            document=instance,
            block_type=Block.BlockType.PARAGRAPH,
            properties={"text": ""},
            created_by=instance.author,
        )
        instance.content = [block.id]
        instance.save(update_fields=["content"])
