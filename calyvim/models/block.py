from django.db import models
from django.contrib.postgres.fields import ArrayField

from calyvim.models.base import UUIDTimestampModel


class Block(UUIDTimestampModel):
    class BlockType(models.TextChoices):
        HEADING_1 = ("heading_1", "Heading 1")
        HEADING_2 = ("heading_2", "Heading 2")
        HEADING_3 = ("heading_3", "Heading 3")
        PARAGRAPH = ("paragraph", "Paragraph")
        QUOTE = ("quote", "Quote")
        TOGGLE = ("toggle", "Toggle")
        BULLETED_LIST = ("bullet_list", "Bullet List")
        NUMBERED_LIST = ("numbered_list", "Numbered List")
        CODE = ("code", "Code")
        LINK = ("link", "Link")
        PAGE = ("page", "Page")

    document = models.ForeignKey(
        "Document", on_delete=models.CASCADE, related_name="blocks"
    )
    page = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="page_blocks",
    )
    block_type = models.CharField(
        max_length=24, choices=BlockType.choices, default=BlockType.PARAGRAPH
    )
    content = ArrayField(base_field=models.UUIDField(), default=list)
    properties = models.JSONField()
    created_by = models.ForeignKey(
        "User", on_delete=models.SET_NULL, null=True, related_name="created_blocks"
    )

    class Meta:
        db_table = "blocks"

    def __str__(self):
        return str(self.id)
