from django.db import transaction
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.utils.html import strip_tags
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
    TaskSnapshot,
)
from calyvim.mixins import BoardMixin
from calyvim.api.tasks.serializers import (
    TaskSerializer,
    TaskSequenceUpdateSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskCommentSerializer,
    StateSerializer,
    MemberSerializer,
    PrioritySerializer,
    LabelSerializer,
    SprintSerializer,
    AttachmentSerializer,
    CommentSerializer,
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
            case "share_link":
                return [
                    IsAuthenticated(),
                    BoardGenericPermission(
                        allowed_roles=[
                            BoardPermissionRole.ADMIN,
                            BoardPermissionRole.MAINTAINER,
                            BoardPermissionRole.COLLABORATOR,
                            BoardPermissionRole.GUEST,
                        ]
                    ),
                ]
            case _:
                return super().get_permissions()

    def create(self, request, *args, **kwargs):
        create_serializer = TaskCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
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

        task = Task(**data, created_by=request.user, board=request.board)
        task.save()

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
        response_data = {
            "task": serializer.data,
        }

        if request.query_params.getlist("include[]"):
            for item in request.query_params.getlist("include[]"):
                match item:
                    case "attachments":
                        attachments = task.attachments.all()
                        response_data["attachments"] = AttachmentSerializer(
                            attachments, many=True
                        ).data
                    case "subtasks":
                        subtasks = task.subtasks.all()
                        response_data["subtasks"] = TaskSerializer(
                            subtasks, many=True
                        ).data
                    case "comments":
                        comments = TaskComment.objects.filter(
                            task=task, comment_type="update"
                        ).order_by("-created_at")
                        response_data["comments"] = CommentSerializer(
                            comments, many=True
                        ).data

        return Response(response_data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        parent_id = request.query_params.get("parent_id", None)
        queryset = Task.objects.filter(
            board=request.board, archived_at__isnull=True, parent_id=parent_id
        )
        tasks = (
            queryset.prefetch_related("assignees", "labels")
            .select_related("priority", "created_by", "estimate", "sprint", "assignee")
            .order_by("sequence")
        )
        serializer = TaskSerializer(tasks, many=True)
        response_data = {
            "results": serializer.data,
        }
        return Response(data=response_data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def kanban(self, request, *args, **kwargs):
        parent_id = request.query_params.get("parent_id", None)
        queryset = Task.objects.filter(
            board=request.board, archived_at__isnull=True, parent_id=parent_id
        )
        group_by = request.query_params.get("group_by", None)
        if request.query_params.getlist("assignees[]"):
            # Filter for assignees
            assignees = request.query_params.getlist("assignees[]")
            queryset = queryset.filter(assignee__in=assignees)

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
            queryset = queryset.filter(sprint__in=sprints)

        tasks = queryset.select_related(
            "priority", "created_by", "estimate", "sprint", "assignee"
        ).order_by("sequence")
        results = []

        states = request.board.states.all()
        if not group_by:
            for state in states:
                state_tasks = [task for task in tasks if task.state_id == state.id]
                results.append(
                    {
                        **StateSerializer(state).data,
                        "tasks": TaskSerializer(state_tasks, many=True).data,
                    }
                )

        elif group_by == "assignee":
            assignees = request.board.members
            for assignee in assignees:
                states_data = []
                member_tasks = [
                    task for task in tasks if task.assignee_id == assignee.id
                ]
                for state in states:
                    state_tasks = [
                        task for task in member_tasks if task.state_id == state.id
                    ]
                    states_data.append(
                        {
                            **StateSerializer(state).data,
                            "tasks": TaskSerializer(state_tasks, many=True).data,
                        }
                    )

                results.append(
                    {
                        "group_key": assignee.id,
                        "states": states_data,
                        "group_by": group_by,
                        "assignee": MemberSerializer(assignee).data,
                    }
                )
            unassigned_tasks = [task for task in tasks if task.assignee_id is None]
            states_data = []
            for state in states:
                state_tasks = [
                    task for task in unassigned_tasks if task.state_id == state.id
                ]
                states_data.append(
                    {
                        **StateSerializer(state).data,
                        "tasks": TaskSerializer(state_tasks, many=True).data,
                    }
                )
            results.append(
                {
                    "group_key": "no_assignee",
                    "states": states_data,
                    "group_by": group_by,
                    "assignee": None,
                }
            )

        elif group_by == "priority":
            priorities = request.board.priorities.all()
            for priority in priorities:
                priority_tasks = [
                    task for task in tasks if task.priority_id == priority.id
                ]
                states_data = []
                for state in states:
                    state_tasks = [
                        task for task in priority_tasks if task.state_id == state.id
                    ]
                    states_data.append(
                        {
                            **StateSerializer(state).data,
                            "tasks": TaskSerializer(state_tasks, many=True).data,
                        }
                    )
                results.append(
                    {
                        "group_key": priority.id,
                        "states": states_data,
                        "group_by": group_by,
                        "priority": PrioritySerializer(priority).data,
                    }
                )
            unprioritized_tasks = [task for task in tasks if task.priority_id is None]
            states_data = []
            for state in states:
                state_tasks = [
                    task for task in unprioritized_tasks if task.state_id == state.id
                ]
                states_data.append(
                    {
                        **StateSerializer(state).data,
                        "tasks": TaskSerializer(state_tasks, many=True).data,
                    }
                )
            results.append(
                {
                    "group_key": "no_priority",
                    "states": states_data,
                    "group_by": group_by,
                    "priority": None,
                }
            )

        elif group_by == "task_type":
            task_types = [choice[0] for choice in Task.TaskType.choices]
            for task_type in task_types:
                task_type_tasks = [
                    task for task in tasks if task.task_type == task_type
                ]
                states_data = []
                for state in states:
                    state_tasks = [
                        task for task in task_type_tasks if task.state_id == state.id
                    ]
                    states_data.append(
                        {
                            **StateSerializer(state).data,
                            "tasks": TaskSerializer(state_tasks, many=True).data,
                        }
                    )
                results.append(
                    {
                        "group_key": task_type,
                        "states": states_data,
                        "group_by": group_by,
                        "task_type": dict(Task.TaskType.choices).get(task_type),
                    }
                )

        elif group_by == "sprint":
            sprints = request.board.sprints.all().order_by("-created_at")
            for sprint in sprints:
                sprint_tasks = [task for task in tasks if task.sprint_id == sprint.id]
                states_data = []
                for state in states:
                    state_tasks = [
                        task for task in sprint_tasks if task.state_id == state.id
                    ]
                    states_data.append(
                        {
                            **StateSerializer(state).data,
                            "tasks": TaskSerializer(state_tasks, many=True).data,
                        }
                    )
                results.append(
                    {
                        "group_key": sprint.id,
                        "states": states_data,
                        "group_by": group_by,
                        "sprint": SprintSerializer(sprint).data,
                    }
                )
            no_sprint_tasks = [task for task in tasks if task.sprint_id is None]
            states_data = []
            for state in states:
                state_tasks = [
                    task for task in no_sprint_tasks if task.state_id == state.id
                ]
                states_data.append(
                    {
                        **StateSerializer(state).data,
                        "tasks": TaskSerializer(state_tasks, many=True).data,
                    }
                )
            results.append(
                {
                    "group_key": "no_sprint",
                    "states": states_data,
                    "group_by": group_by,
                    "sprint": None,
                }
            )

        response_data = {
            "results": results,
        }

        return Response(response_data, status=status.HTTP_200_OK)

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
                if not value:
                    task_updates.append(f"removed priority {task.priority.name}.")
                else:
                    priority = get_object_or_raise_api_404(
                        Priority, board=request.board, id=value
                    )
                    if task.priority:
                        task_updates.append(
                            f"changed priority from {task.priority.name} to {priority.name}."
                        )
                    else:
                        task_updates.append(f"has set task priority as {priority.name}")

            if key == "assignee_id":
                if not value:
                    task_updates.append(
                        f"removed assignee {task.assignee.display_name}."
                    )
                else:
                    assignee = request.board.members.filter(id=value).first()
                    if task.assignee:
                        task_updates.append(
                            f"changed assignee from {task.assignee.display_name} to {assignee.display_name}."
                        )
                    else:
                        task_updates.append(f"assigned to {assignee.display_name}.")

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
                today = timezone.now().date()
                snapshot, created = TaskSnapshot.objects.get_or_create(
                    task=task, date=today, defaults={"state": state}
                )
                if not created:
                    snapshot.state = state
                    snapshot.save(update_fields=["state"])

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

        if "description" in data:
            task.description_raw = strip_tags(data["description"])
            task.save(update_fields=["description_raw"])

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
            TaskComment.objects.create(
                task=task,
                content=", ".join(task_updates),
                author=request.user,
                comment_type=TaskComment.CommentType.ACTIVITY,
            )
        response_data = {
            "detail": "Task updated successfully.",
            "log": ", ".join(task_updates),
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
        old_state = task.state
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

        # Check for valid state Id and Update State Task Log
        if data.get("state_id"):
            state = get_object_or_raise_api_404(
                State, board=request.board, id=data.get("state_id")
            )
            if old_state != state:
                today = timezone.now().date()
                snapshot, created = TaskSnapshot.objects.get_or_create(
                    task=task, date=today, defaults={"state": state}
                )
                if not created:
                    snapshot.state = state
                    snapshot.save(update_fields=["state"])

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

    @action(methods=["GET"], detail=True, url_path="share-link")
    def share_link(self, request, *args, **kwargs):
        task = get_object_or_raise_api_404(
            Task, board=request.board, id=kwargs.get("pk")
        )
        shareable_link = f"{settings.BASE_URL}/boards/{task.board.id}/tasks/{task.name}"
        response_data = {
            "detail": f"Shareable link for {task.name} generated successfully.",
            "share_link": shareable_link,
        }
        return Response(
            data=response_data,
            status=status.HTTP_200_OK,
        )
