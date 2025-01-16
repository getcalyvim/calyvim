from django.db.models.signals import post_save
from django.dispatch import receiver
from calyvim.models import TeamMembership, BoardTeamPermission, BoardPermission


@receiver(post_save, sender=TeamMembership)
def assign_board_permissions_on_team_membership_creation(
    sender, instance, created, **kwargs
):
    if created:
        board_team_permissions = BoardTeamPermission.objects.filter(team=instance.team)
        for board_team_permission in board_team_permissions:
            BoardPermission.objects.create(
                board=board_team_permission.board,
                role=board_team_permission.role,
                team_permission=board_team_permission,
                team_membership=instance,
                user=instance.user,
            )


@receiver(post_save, sender=BoardTeamPermission)
def create_or_update_board_permission(sender, instance, created, **kwargs):
    if created:
        team_memberships = instance.team.memberships.all()
        for team_membership in team_memberships:
            BoardPermission.objects.create(
                board=instance.board,
                role=instance.role,
                team_permission=instance,
                team_membership=team_membership,
                user=team_membership.user,
            )
    else:
        BoardPermission.team_objects.filter(
            board=instance.board, team_permission=instance
        ).update(role=instance.role)
