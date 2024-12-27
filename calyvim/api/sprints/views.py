from django.db import transaction
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from calyvim.models import Sprint
from calyvim.mixins import BoardMixin
from calyvim.api.sprints.serializers import SprintSerializer, SprintCreateSerializer
from calyvim.permissions import BoardGenericPermission
from calyvim.exceptions import InvalidInputException
from calyvim.utils import get_object_or_raise_api_404


class SprintsViewSet(BoardMixin, ViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        match self.action:
            case "list":
                return [IsAuthenticated(), BoardGenericPermission()]
            case "create":
                return [
                    IsAuthenticated(),
                    BoardGenericPermission(allowed_roles=["admin", "maintainer"]),
                ]
            case "destroy":
                return [
                    IsAuthenticated(),
                    BoardGenericPermission(allowed_roles=["admin", "maintainer"]),
                ]
            case "archive":
                return [
                    IsAuthenticated(),
                    BoardGenericPermission(allowed_roles=["admin", "maintainer"]),
                ]
            case "activate":
                return [
                    IsAuthenticated(),
                    BoardGenericPermission(allowed_roles=["admin", "maintainer"]),
                ]
            case _:
                return super().get_permissions()

    def create(self, request, *args, **kwargs):
        create_serializer = SprintCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            raise InvalidInputException

        data = create_serializer.validated_data
        with transaction.atomic():
            if data.get("is_active"):
                Sprint.objects.filter(board=request.board, is_active=True).update(
                    is_active=False
                )

            sprint = Sprint.objects.create(
                board=request.board,
                **data,
            )

        serializer = SprintSerializer(sprint)
        response_data = {
            "detail": f"The sprint '{sprint.name}' has been created successfully.",
            "sprint": serializer.data,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        sprints = Sprint.objects.filter(board=request.board).order_by("-created_at")
        serializer = SprintSerializer(sprints, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        sprint = get_object_or_raise_api_404(
            Sprint, board=request.board, pk=kwargs["pk"]
        )
        if sprint.is_active:
            return Response(
                {"detail": "The active sprint cannot be deleted."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        sprint.delete()
        response_data = {
            "detail": f"The sprint '{sprint.name}' has been deleted successfully."
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)

    @action(methods=["PATCH"], detail=True)
    def archive(self, request, *args, **kwargs):
        sprint = get_object_or_raise_api_404(
            Sprint, board=request.board, pk=kwargs["pk"]
        )
        if sprint.is_active:
            return Response(
                {"detail": "The active sprint cannot be archived."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        sprint.archive()
        response_data = {
            "detail": f"The sprint '{sprint.name}' has been archived successfully."
        }
        return Response(response_data, status=status.HTTP_200_OK)

    @action(methods=["PATCH"], detail=True)
    def activate(self, request, *args, **kwargs):
        sprint = get_object_or_raise_api_404(
            Sprint, board=request.board, pk=kwargs["pk"]
        )

        with transaction.atomic():
            Sprint.objects.filter(board=request.board, is_active=True).update(
                is_active=False
            )
            sprint.is_active = True
            sprint.save()

        serializer = SprintSerializer(sprint)
        response_data = {
            "detail": f"The sprint '{sprint.name}' has been activated successfully.",
            "sprint": serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)
