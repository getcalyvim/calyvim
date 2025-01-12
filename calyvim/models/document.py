from django.db import models
from django.contrib.postgres.fields import ArrayField

from calyvim.models.base import UUIDTimestampModel
from calyvim.models.choice import DocumentPermissionRole


class Document(UUIDTimestampModel):
    workspace = models.ForeignKey(
        "Workspace", on_delete=models.CASCADE, related_name="documents"
    )
    name = models.CharField(max_length=255)
    author = models.ForeignKey(
        "User", on_delete=models.SET_NULL, related_name="created_documents", null=True
    )
    description = models.TextField(blank=True, null=True)
    content = ArrayField(base_field=models.UUIDField(), default=list, blank=True)

    class Meta:
        db_table = "documents"

    def __str__(self):
        return f"{self.name}"


class DocumentTeamPermission(UUIDTimestampModel):
    document = models.ForeignKey(
        "Document", on_delete=models.CASCADE, related_name="team_memberships"
    )
    team = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="team_document_team_memberships"
    )
    role = models.CharField(
        max_length=20,
        choices=DocumentPermissionRole.choices,
        default=DocumentPermissionRole.VIEWER,
    )

    class Meta:
        db_table = "document_team_permissions"


class DocumentPermission(UUIDTimestampModel):
    document = models.ForeignKey(
        "Document", on_delete=models.CASCADE, related_name="permissions"
    )
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_document_permissions"
    )
    team_permission = models.ForeignKey(
        "DocumentTeamPermission",
        related_name="+",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    workspace_membership = models.ForeignKey(
        "WorkspaceMembership",
        related_name="+",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    team_membership = models.ForeignKey(
        "TeamMembership",
        related_name="+",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=20,
        choices=DocumentPermissionRole.choices,
        default=DocumentPermissionRole.VIEWER,
    )

    class Meta:
        db_table = "document_permissions"

    def __str__(self):
        return str(self.id)
