from django.urls import path
from calyvim.views.workspaces import (
    WorkspaceDashboardView,
    WorkspaceMembersView,
    WorkspaceTeamsView,
    WorkspaceTeamsEditView,
    WorkspaceSettingsGeneralView,
    WorkspaceSettingsBillingView,
    WorkspaceMemberConfirmationView,
    WorkspaceLeaveView,
    WorkspaceCreateView,
    WorkspaceIndexView,
    WorkspaceDeleteView,
    WorkspaceBoardsView,
    WorkspaceNewslinesView,
    WorkspaceTodosView,
    WorkspaceDocumentsView
)

# fmt: off
urlpatterns = [
    path("create/", WorkspaceCreateView.as_view(), name="workspace-create"),
    path("<str:workspace_slug>/", WorkspaceDashboardView.as_view(), name="workspaces-dashboard"),
    path("<str:workspace_slug>/boards/", WorkspaceBoardsView.as_view(), name="workspace-boards"),
    path("<str:workspace_slug>/newslines/", WorkspaceNewslinesView.as_view(), name="workspace-newslines"),
    path("<str:workspace_slug>/todos/", WorkspaceTodosView.as_view(), name="workspace-todos"),
    path("<str:workspace_slug>/documents/", WorkspaceDocumentsView.as_view(), name="workspace-documents"),
    path("<str:workspace_slug>/settings/", WorkspaceSettingsGeneralView.as_view(), name="workspaces-settings-general"),
    path("<str:workspace_slug>/settings/billing/", WorkspaceSettingsBillingView.as_view(), name="workspaces-settings-billing"),
    path("<str:workspace_slug>/settings/members/", WorkspaceMembersView.as_view(), name="workspaces-members"),
    path("<str:workspace_slug>/settings/teams/", WorkspaceTeamsView.as_view(), name="workspaces-teams"),
    path("<str:workspace_slug>/settings/teams/<uuid:team_id>/edit/", WorkspaceTeamsEditView.as_view(), name="workspaces-teams-edit"),
    path("<str:workspace_slug>/members/<str:invitation_id>/confirm/", WorkspaceMemberConfirmationView.as_view(), name="workspaces-member-confirmation"),
    path("<str:workspace_slug>/leave/", WorkspaceLeaveView.as_view(), name="workspaces-leave"),
    path("<str:workspace_slug>/delete/", WorkspaceDeleteView.as_view(), name="workspace-delete"),
    path("", WorkspaceIndexView.as_view(), name="workspace-index"),
]
