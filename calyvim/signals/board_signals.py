from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from calyvim.models import (
    Board,
    BoardPermission,
    WorkspaceMembership,
    State,
    Priority,
    Estimate,
)


@receiver(post_save, sender=Board)
def create_board_admin(sender, instance, created, **kwargs):
    if created:
        workspace_membership = WorkspaceMembership.objects.filter(
            user=instance.created_by, workspace=instance.workspace
        ).first()

        if not workspace_membership:
            raise ObjectDoesNotExist("No membership found for the user")

        BoardPermission.objects.create(
            board=instance,
            user=instance.created_by,
            role="admin",
            workspace_membership=workspace_membership,
        )


@receiver(post_save, sender=Board)
def setup_initial_project(sender, instance, created, **kwargs):
    if created:
        if not instance.is_from_template:
            # Create initial states
            State.objects.bulk_create(
                [
                    State(
                        board=instance,
                        name="Backlog",
                        sequence=10000,
                        category=State.Category.OPEN,
                    ),
                    State(
                        board=instance,
                        name="Todo",
                        sequence=20000,
                        category=State.Category.OPEN,
                    ),
                    State(
                        board=instance,
                        name="In-progress",
                        sequence=30000,
                        category=State.Category.ACTIVE,
                    ),
                    State(
                        board=instance,
                        name="Review",
                        sequence=40000,
                        category=State.Category.ACTIVE,
                    ),
                    State(
                        board=instance,
                        name="Done",
                        sequence=50000,
                        category=State.Category.COMPLETED,
                    ),
                ]
            )

            # Create initial priorities
            Priority.objects.bulk_create(
                [
                    Priority(board=instance, name="Urgent"),
                    Priority(board=instance, name="High"),
                    Priority(board=instance, name="Medium"),
                    Priority(board=instance, name="Low"),
                ]
            )

            # Create initial estimates
            Estimate.objects.bulk_create(
                [
                    Estimate(board=instance, key=1, value="1h"),
                    Estimate(board=instance, key=2, value="2h"),
                    Estimate(board=instance, key=3, value="4h"),
                    Estimate(board=instance, key=4, value="1d"),
                    Estimate(board=instance, key=5, value="2d"),
                    Estimate(board=instance, key=6, value="4d"),
                ]
            )
        else:
            template_board = instance.template
            print("Template Board --> ", template_board)
