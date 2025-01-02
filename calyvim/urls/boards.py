from django.urls import path
from calyvim.views.boards import (
    BoardKanbanView,
    BoardTableView,
    BoardSettingsGeneralView,
    BoardSettingsCollaboratorsView,
    BoardSettingsStatesView,
    BoardSprintsListView,
    BoardSprintsDetailView,
    BoardSettingsPrioritiesView,
    BoardLeaveView,
    BoardDeleteView,
    BoardTasksDetailView
)

# fmt: off
urlpatterns = [
    path("table/", BoardTableView.as_view(), name="board-table"),
    path("sprints/", BoardSprintsListView.as_view(), name="board-sprint-list"),
    path("sprints/<uuid:sprint_id>/", BoardSprintsDetailView.as_view(), name="board-sprint-detail"),
    path("settings/", BoardSettingsGeneralView.as_view(), name="board-settings-general"),
    path("settings/collaborators/", BoardSettingsCollaboratorsView.as_view(), name="board-settings-collaborators"),
    path("settings/states/", BoardSettingsStatesView.as_view(), name="board-settings-states"),
    path("settings/priorities/", BoardSettingsPrioritiesView.as_view(), name="board-settings-priorities"),
    path("leave/", BoardLeaveView.as_view(), name="board-leave"),
    path("delete/", BoardDeleteView.as_view(), name="board-delete"),
    path("tasks/<str:task_name>/", BoardTasksDetailView.as_view(), name="board-tasks-detail"),
    path("", BoardKanbanView.as_view(), name="board-kanban"),
]