from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from calyvim.models import Label
from calyvim.mixins import BoardMixin
from calyvim.api.labels.serializers import LabelSerializer
from calyvim.permissions import BoardGenericPermission


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
            case _:
                return super().get_permissions()

    def list(self, request, *args, **kwargs):
        labels = Label.objects.filter(board=request.board).order_by("name")
        serializer = LabelSerializer(labels, many=True)
        response_data = {
            "results": serializer.data,
        }
        return Response(data=response_data, status=status.HTTP_200_OK)
