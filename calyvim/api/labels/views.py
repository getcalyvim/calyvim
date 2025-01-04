from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from calyvim.models import Label
from calyvim.mixins import BoardMixin
from calyvim.api.labels.serializers import LabelSerializer, LabelCreateSerializer
from calyvim.permissions import BoardGenericPermission
from calyvim.exceptions import InvalidInputException


class LabelsViewSet(BoardMixin, ViewSet):
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
            case _:
                return super().get_permissions()

    def list(self, request, *args, **kwargs):
        labels = Label.objects.filter(board=request.board).order_by("name")
        serializer = LabelSerializer(labels, many=True)
        response_data = {
            "results": serializer.data,
        }
        return Response(data=response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        create_serializer = LabelCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            raise InvalidInputException
        data = create_serializer.validated_data
        if Label.objects.filter(board=request.board, name=data["name"]).exists():
            return Response(
                data={
                    "detail": "Label with this name already exists.",
                    "errors": ["Duplicate label name in the board."],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        label = Label.objects.create(board=request.board, **data)
        serializer = LabelSerializer(label)
        response_data = {
            "label": serializer.data,
            "detail": "Label created successfully.",
        }
        return Response(data=response_data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        label = Label.objects.get(id=kwargs["pk"], board=request.board)
        label.delete()
        return Response(
            data={"detail": "Label deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
