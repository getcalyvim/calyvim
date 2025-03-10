from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from calyvim.models import WorkspaceMembership, Board, Sprint, BoardPermission, Task
from calyvim.serializers import (
    WorkspaceSerializer,
    ProfileSerializer,
    BoardSerializer,
    SprintSerializer,
    MinimalTaskSerializer,
)
from calyvim.mixins import BoardPermissionMixin


# @method_decorator(cache_page(60 * 15, key_prefix="boards"), name="dispatch")
class BoardTasksListView(LoginRequiredMixin, BoardPermissionMixin, View):
    def get(self, request, *args, **kwargs):
        board = get_object_or_404(Board, id=kwargs.get("board_id"))

        if not self.has_valid_board_permission(board, request.user):
            raise Http404

        context = {
            "props": {
                "workspace": WorkspaceSerializer(board.workspace).data,
                "board": BoardSerializer(board).data,
                "current_user": ProfileSerializer(request.user).data,
            }
        }
        return render(request, "boards/tasks/list.html", context)


class BoardTableView(LoginRequiredMixin, BoardPermissionMixin, View):
    def get(self, request, *args, **kwargs):
        board = get_object_or_404(Board, id=kwargs.get("board_id"))

        if not self.has_valid_board_permission(board, request.user):
            raise Http404

        context = {
            "props": {
                "workspace": WorkspaceSerializer(board.workspace).data,
                "board": BoardSerializer(board).data,
            }
        }
        return render(request, "boards/table.html", context)


class BoardSprintsListView(LoginRequiredMixin, BoardPermissionMixin, View):
    def get(self, request, *args, **kwargs):
        board = get_object_or_404(Board, id=kwargs.get("board_id"))

        if not self.has_valid_board_permission(board, request.user):
            raise Http404

        context = {
            "props": {
                "workspace": WorkspaceSerializer(board.workspace).data,
                "board": BoardSerializer(board).data,
            }
        }
        return render(request, "boards/sprints/list.html", context)


class BoardSprintsDetailView(LoginRequiredMixin, BoardPermissionMixin, View):
    def get(self, request, *args, **kwargs):
        board = get_object_or_404(Board, id=kwargs.get("board_id"))
        sprint = get_object_or_404(Sprint, id=kwargs.get("sprint_id"), board=board)

        if not self.has_valid_board_permission(board, request.user):
            raise Http404

        # If the board's current grouping is by "sprint", it resets the grouping to None and updates the board.
        if board.current_group_by == "sprint":
            board.current_group_by = None
            board.save(update_fields=["current_group_by"])

        context = {
            "props": {
                "workspace": WorkspaceSerializer(board.workspace).data,
                "board": BoardSerializer(board).data,
                "sprint": SprintSerializer(sprint).data,
            }
        }
        return render(request, "boards/sprints/detail.html", context)


class BoardSettingsGeneralView(LoginRequiredMixin, BoardPermissionMixin, View):
    def get(self, request, *args, **kwargs):
        board = get_object_or_404(Board, id=kwargs.get("board_id"))

        if not self.has_valid_board_permission(board, request.user):
            raise Http404

        # Check permission
        has_edit_permission = self.has_valid_board_permission(
            board, request.user, allowed_roles=["admin", "maintainer"]
        )

        context = {
            "props": {
                "workspace": WorkspaceSerializer(board.workspace).data,
                "board": BoardSerializer(board).data,
                "has_edit_permission": has_edit_permission,
            }
        }
        return render(request, "boards/settings/general.html", context)


class BoardSettingsCollaboratorsView(LoginRequiredMixin, BoardPermissionMixin, View):
    def get(self, request, *args, **kwargs):
        board = get_object_or_404(Board, id=kwargs.get("board_id"))

        if not self.has_valid_board_permission(board, request.user):
            raise Http404

        # Check permission
        has_edit_permission = self.has_valid_board_permission(
            board, request.user, allowed_roles=["admin", "maintainer"]
        )

        context = {
            "props": {
                "workspace": WorkspaceSerializer(board.workspace).data,
                "board": BoardSerializer(board).data,
                "has_edit_permission": has_edit_permission,
            }
        }
        return render(request, "boards/settings/collaborators.html", context)


class BoardSettingsStatesView(LoginRequiredMixin, BoardPermissionMixin, View):
    def get(self, request, *args, **kwargs):
        board = get_object_or_404(Board, id=kwargs.get("board_id"))

        if not self.has_valid_board_permission(board, request.user):
            raise Http404

        # Check permission
        has_edit_permission = self.has_valid_board_permission(
            board, request.user, allowed_roles=["admin", "maintainer"]
        )

        context = {
            "props": {
                "workspace": WorkspaceSerializer(board.workspace).data,
                "board": BoardSerializer(board).data,
                "has_edit_permission": has_edit_permission,
            }
        }
        return render(request, "boards/settings/states.html", context)


class BoardSettingsPrioritiesView(LoginRequiredMixin, BoardPermissionMixin, View):
    def get(self, request, *args, **kwargs):
        board = get_object_or_404(Board, id=kwargs.get("board_id"))

        if not self.has_valid_board_permission(board, request.user):
            raise Http404

        # Check permission
        has_edit_permission = self.has_valid_board_permission(
            board, request.user, allowed_roles=["admin", "maintainer"]
        )

        context = {
            "props": {
                "workspace": WorkspaceSerializer(board.workspace).data,
                "board": BoardSerializer(board).data,
                "has_edit_permission": has_edit_permission,
            }
        }
        return render(request, "boards/settings/priorities.html", context)


class BoardLeaveView(LoginRequiredMixin, BoardPermissionMixin, View):
    def get(self, request, *args, **kwargs):
        board = get_object_or_404(Board, id=kwargs.get("board_id"))

        if not self.has_valid_board_permission(board, request.user):
            raise Http404

        board_permission = BoardPermission.user_objects.filter(
            board=board, user=request.user
        ).first()
        if not board_permission:
            raise Http404

        admin_count = BoardPermission.user_objects.filter(
            board=board, role="admin"
        ).count()

        if admin_count == 1 and board_permission.role == "admin":
            raise Http404

        board_permission.delete()
        return redirect("workspace-boards", workspace_slug=board.workspace.slug)


class BoardDeleteView(LoginRequiredMixin, BoardPermissionMixin, View):
    def get(self, request, *args, **kwargs):

        board = get_object_or_404(Board, id=kwargs.get("board_id"))
        workspace = board.workspace

        if not self.has_valid_board_permission(board, request.user):
            raise Http404

        board_permission = BoardPermission.user_objects.filter(
            board=board, user=request.user, role="admin"
        ).first()
        if not board_permission:
            raise Http404

        board.delete()
        return redirect("workspace-boards", workspace_slug=workspace.slug)


class BoardTasksDetailView(LoginRequiredMixin, BoardPermissionMixin, View):
    def get(self, request, *args, **kwargs):
        board = get_object_or_404(Board, id=kwargs.get("board_id"))

        if not self.has_valid_board_permission(board, request.user):
            raise Http404

        task = (
            Task.objects.filter(board=board, name=kwargs.get("task_name"))
            .only("id", "name", "number", "created_at")
            .first()
        )
        if not task:
            raise Http404

        context = {
            "props": {
                "workspace": WorkspaceSerializer(board.workspace).data,
                "board": BoardSerializer(board).data,
                "task": MinimalTaskSerializer(task).data,
            }
        }
        return render(request, "boards/tasks/detail.html", context)


class BoardSettingsLabelsView(LoginRequiredMixin, BoardPermissionMixin, View):
    def get(self, request, *args, **kwargs):
        board = get_object_or_404(Board, id=kwargs.get("board_id"))

        if not self.has_valid_board_permission(board, request.user):
            raise Http404

        # Check permission
        has_edit_permission = self.has_valid_board_permission(
            board, request.user, allowed_roles=["admin", "maintainer"]
        )

        context = {
            "props": {
                "workspace": WorkspaceSerializer(board.workspace).data,
                "board": BoardSerializer(board).data,
                "has_edit_permission": has_edit_permission,
            }
        }
        return render(request, "boards/settings/labels.html", context)