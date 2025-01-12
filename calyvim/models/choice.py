from django.db import models


class BoardPermissionRole(models.TextChoices):
    ADMIN = ("admin", "Admin")
    COLLABORATOR = ("collaborator", "Collaborator")
    MAINTAINER = ("maintainer", "Maintainer")
    GUEST = ("guest", "Guest")


class DocumentPermissionRole(models.TextChoices):
    EDITOR = ("editor", "Editor")
    VIEWER = ("viewer", "Viewer")