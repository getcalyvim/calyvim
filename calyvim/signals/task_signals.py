from django.db.models.signals import post_save
from django.dispatch import receiver
from calyvim.models import Task, TaskComment

@receiver(post_save, sender=Task)
def create_task_comment(sender, instance, created, **kwargs):
    if created:
        TaskComment.objects.create(
            task=instance,
            author=instance.created_by,
            content="created the task.",
            comment_type=TaskComment.CommentType.ACTIVITY,
        )