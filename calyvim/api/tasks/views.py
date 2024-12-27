import time
from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from calyvim.utils import get_object_or_raise_api_404
from calyvim.models import (
    Task,
    TaskAssignee,
    State,
    Priority,
    User,
    TaskComment,
    BoardPermissionRole,
    Estimate,
    Sprint,
)
from calyvim.mixins import BoardMixin
from calyvim.api.tasks.serializers import (
    TaskSerializer,
    TaskSequenceUpdateSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskCommentSerializer,
)
from calyvim.permissions import BoardGenericPermission
from calyvim.exceptions import (
    InvalidInputException,
    TaskNotFoundException,
    StateNotFoundException,
    PriorityNotFoundException,
)


class TasksViewSet(BoardMixin, ViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        match self.action:
            case "list":
                return [IsAuthenticated(), BoardGenericPermission()]
            case "create":
                return [
                    IsAuthenticated(),
                    BoardGenericPermission(
                        allowed_roles=[
                            BoardPermissionRole.ADMIN,
                            BoardPermissionRole.COLLABORATOR,
                            BoardPermissionRole.MAINTAINER,
                        ]
                    ),
                ]
            case "retrieve":
                return [IsAuthenticated(), BoardGenericPermission()]
            case "partial_update":
                return [
                    IsAuthenticated(),
                    BoardGenericPermission(
                        allowed_roles=[
                            BoardPermissionRole.ADMIN,
                            BoardPermissionRole.COLLABORATOR,
                            BoardPermissionRole.MAINTAINER,
                        ]
                    ),
                ]
            case "update_sequence":
                return [
                    IsAuthenticated(),
                    BoardGenericPermission(
                        allowed_roles=[
                            BoardPermissionRole.ADMIN,
                            BoardPermissionRole.MAINTAINER,
                        ]
                    ),
                ]

            case "archive":
                return [
                    IsAuthenticated(),
                    BoardGenericPermission(
                        allowed_roles=[
                            BoardPermissionRole.ADMIN,
                            BoardPermissionRole.MAINTAINER,
                            BoardPermissionRole.COLLABORATOR,
                        ]
                    ),
                ]
            case "state":
                return [
                    IsAuthenticated(),
                    BoardGenericPermission(
                        allowed_roles=[
                            BoardPermissionRole.ADMIN,
                            BoardPermissionRole.MAINTAINER,
                            BoardPermissionRole.COLLABORATOR,
                        ]
                    ),
                ]
            case _:
                return super().get_permissions()

    def create(self, request, *args, **kwargs):
        create_serializer = TaskCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            print(create_serializer.errors)
            raise InvalidInputException

        data = create_serializer.validated_data
        # Check for stateId
        if not State.objects.filter(
            board=request.board, id=data.get("state_id")
        ).exists():
            raise StateNotFoundException

        if (
            data.get("priority_id")
            and not Priority.objects.filter(
                board=request.board, id=data.get("priority_id")
            ).exists()
        ):
            raise PriorityNotFoundException

        assignees = data.pop("assignees")
        task = Task(**data, created_by=request.user, board=request.board)
        task.save()
        if assignees:
            task.assignees.set(assignees)

        serializer = TaskSerializer(task)
        response_data = {
            "detail": f"Task '{task.name}' has been created successfully",
            "task": serializer.data,
        }
        return Response(data=response_data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        task = Task.objects.filter(board=request.board, id=kwargs.get("pk")).first()
        if not task:
            raise TaskNotFoundException

        serializer = TaskSerializer(task)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        parent_id = request.query_params.get("parent_id", None)
        queryset = Task.objects.filter(
            board=request.board, archived_at__isnull=True, parent_id=parent_id
        )
        if request.query_params.getlist("assignees[]"):
            # Filter for assignees
            assignees = request.query_params.getlist("assignees[]")
            queryset = queryset.filter(assignees__in=assignees)

        if request.query_params.getlist("task_types[]"):
            # Filter for task type
            task_types = request.query_params.getlist("task_types[]")
            queryset = queryset.filter(task_type__in=task_types)

        if request.query_params.getlist("priorities[]"):
            # Filter form priorities
            priorities = request.query_params.getlist("priorities[]")
            queryset = queryset.filter(priority__in=priorities)

        if request.query_params.getlist("labels[]"):
            # Filter for labels
            labels = request.query_params.getlist("labels[]")
            queryset = queryset.filter(labels__in=labels)

        if request.query_params.getlist("estimates[]"):
            # Filter for estimates
            estimates = request.query_params.getlist("estimates[]")
            queryset = queryset.filter(estimate__in=estimates)

        if request.query_params.getlist("sprints[]"):
            # Filter for sprints
            sprints = request.query_params.getlist("sprints[]")
            queryset = queryset.filter(Q(sprint__in=sprints) | Q(sprint=None))
        else:
            queryset = queryset.filter(sprint=None)

        tasks = (
            queryset.prefetch_related("assignees", "labels")
            .select_related("priority", "created_by", "estimate", "sprint")
            .order_by("sequence")
        )
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        update_serializer = TaskUpdateSerializer(data=request.data)
        if not update_serializer.is_valid():
            raise InvalidInputException

        task = get_object_or_raise_api_404(
            Task, board=request.board, id=kwargs.get("pk"), message="Task not found."
        )

        data = update_serializer.validated_data
        task_updates = []
        assignee_ids = None
        if data.get("assignee_ids"):
            assignee_ids = data.pop("assignee_ids")
        for key, value in data.items():
            if key == "estimate_id":
                estimate = get_object_or_raise_api_404(
                    Estimate, board=request.board, id=value
                )
                if task.estimate:
                    task_updates.append(
                        f"changed estimate from {task.estimate.value} to {estimate.value}"
                    )
                else:
                    task_updates.append(f"has set estimate as {estimate.value}")
            if key == "priority_id":
                priority = get_object_or_raise_api_404(
                    Priority, board=request.board, id=value
                )
                if task.priority:
                    task_updates.append(
                        f"changed priority from {task.priority.name} to {priority.name}."
                    )
                else:
                    task_updates.append(f"has set task priority as {priority.name}")

            if key == "task_type":
                task_updates.append(
                    f"changed task type from {task.task_type} to {value}."
                )

            if key == "state_id":
                state = get_object_or_raise_api_404(
                    State, board=request.board, id=value
                )
                task_updates.append(
                    f"changed state from {task.state.name} to {state.name}."
                )

            if key == "sprint_id":
                if value:
                    sprint = get_object_or_raise_api_404(
                        Sprint, board=request.board, id=value
                    )
                    if not task.sprint:
                        task_updates.append(f"added to sprint {sprint.name}.")
                    else:
                        task_updates.append(f"moved to sprint {sprint.name}.")
                else:
                    task_updates.append(f"removed from sprint {task.sprint.name}.")

            if key == "description":
                TaskComment.objects.create(
                    task=task,
                    content="updated the description.",
                    author=request.user,
                    comment_type=TaskComment.CommentType.ACTIVITY,
                )
                task_updates.append(f"updated description.")

            if key == "summary":
                task_updates.append(f"updated summary.")

            setattr(task, key, value)
        task.save(update_fields=data.keys())
        if assignee_ids:
            current_assignees = set(task.assignees.values_list("id", flat=True))
            new_assignees = set(assignee_ids)
            added_assignees = new_assignees - current_assignees
            removed_assignees = current_assignees - new_assignees

            if added_assignees or removed_assignees:
                task.assignees.set(task.board.members.filter(id__in=assignee_ids))
                if added_assignees:
                    added_names = ", ".join(
                        task.board.members.filter(id__in=added_assignees).values_list(
                            "display_name", flat=True
                        )
                    )
                    task_updates.append(f"added assignees: {added_names}")

                if removed_assignees:
                    removed_names = ", ".join(
                        task.board.members.filter(id__in=removed_assignees).values_list(
                            "display_name", flat=True
                        )
                    )
                    task_updates.append(f"removed assignees: {removed_names}")

        if task_updates:
            comments = TaskComment.objects.bulk_create(
                [
                    TaskComment(
                        task=task,
                        content=update,
                        author=request.user,
                        comment_type=TaskComment.CommentType.ACTIVITY,
                    )
                    for update in task_updates
                ],
            )
        task_serializer = TaskSerializer(task)
        comments_serializer = TaskCommentSerializer(comments, many=True)
        response_data = {
            "task": task_serializer.data,
            "comments": comments_serializer.data,
            "detail": "Task updated successfully.",
        }
        return Response(
            data=response_data,
            status=status.HTTP_200_OK,
        )

    @action(methods=["PATCH"], detail=True, url_path="update-sequence")
    def update_sequence(self, request, *args, **kwargs):
        update_serializer = TaskSequenceUpdateSerializer(data=request.data)
        if not update_serializer.is_valid():
            raise InvalidInputException
        task = get_object_or_raise_api_404(
            Task, board=request.board, id=kwargs.get("pk")
        )
        data = update_serializer.validated_data

        if data.get("previous_task") and data.get("next_task"):
            previous_task = get_object_or_raise_api_404(
                Task, board=request.board, id=data.get("previous_task")
            )
            next_task = get_object_or_raise_api_404(
                Task, board=request.board, id=data.get("next_task")
            )
            task.sequence = (previous_task.sequence + next_task.sequence) / 2

        elif data.get("previous_task"):
            previous_task = get_object_or_raise_api_404(
                Task, board=request.board, id=data.get("previous_task")
            )
            task.sequence = previous_task.sequence + 10000

        elif data.get("next_task"):
            next_task = get_object_or_raise_api_404(
                Task, board=request.board, id=data.get("next_task")
            )
            task.sequence = next_task.sequence / 2

        task.state_id = data.get("state_id")
        task.save(update_fields=["state_id", "sequence"])
        return Response(
            data={"detail": "Task sequence updated", "new_sequence": task.sequence},
            status=status.HTTP_200_OK,
        )

    @action(methods=["PATCH"], detail=True, url_path="archive")
    def archive(self, request, *args, **kwargs):
        task = get_object_or_raise_api_404(
            Task, board=request.board, id=kwargs.get("pk")
        )
        task.archive()
        return Response(
            data={"detail": "Task archived successfully"}, status=status.HTTP_200_OK
        )

    @transaction.atomic
    @action(methods=["PATCH"], detail=False)
    def state(self, request, *args, **kwargs):
        state_id = request.query_params.get("state_id")
        task_ids = request.data.get("task_ids", [])

        if not state_id or not task_ids:
            return Response(
                data={"detail": "State ID's and Task ID's are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        state = get_object_or_raise_api_404(State, board=request.board, id=state_id)
        tasks = Task.objects.filter(board=request.board, id__in=task_ids)

        # Find the last task in the new state
        last_task_in_state = (
            Task.objects.filter(board=request.board, state=state)
            .order_by("-sequence")
            .first()
        )
        new_sequence = (
            last_task_in_state.sequence + 10000 if last_task_in_state else 10000
        )

        task_comments = []
        for task in tasks:
            task.state_id = state.id
            task.sequence = new_sequence
            task.save(update_fields=["state_id", "sequence"])
            new_sequence += 10000

            # Create a TaskComment for each task
            task_comments.append(
                TaskComment(
                    task=task,
                    content=f"State changed to {state.name}",
                    comment_type="activity",
                    author=request.user,
                )
            )

        # Use bulk update to save all tasks at once
        Task.objects.bulk_update(tasks, ["state_id", "sequence"])
        TaskComment.objects.bulk_create(task_comments)

        new_tasks = Task.objects.filter(board=request.board, id__in=task_ids)
        serializer = TaskSerializer(new_tasks, many=True)

        task_names = ", ".join(task.name for task in new_tasks)
        return Response(
            data={
                "detail": f"Tasks ({task_names}) state changed to {state.name}",
                "tasks": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
