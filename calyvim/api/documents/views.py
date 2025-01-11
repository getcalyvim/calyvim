from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from calyvim.api.documents.serializers import DocumentSerializer
from calyvim.permissions import BoardGenericPermission
from calyvim.models import Document, WorkspaceMembership, Workspace
from calyvim.utils import get_object_or_raise_api_404
from calyvim.exceptions import InvalidInputException


class DocumentsViewSet(ViewSet):
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

    def get_workspace_membership(self, user, workspace):
        workspace_membership = get_object_or_raise_api_404(
            WorkspaceMembership, user=user, workspace=workspace
        )
        return workspace_membership

    def list(self, request, *args, **kwargs):
        workspace_id = request.query_params.get("workspace_id")
        if not workspace_id:
            raise InvalidInputException

        workspace = get_object_or_raise_api_404(Workspace, id=workspace_id)

        workspace_membership = self.get_workspace_membership(
            request.user, workspace=workspace
        )
        if workspace_membership.role == "admin":
            documents = Document.objects.filter(workspace=workspace)
        else:
            documents = (
                Document.objects.filter(workspace=workspace)
                .filter(permissions__user=request.user)
                .distinct()
            )

        serializer = DocumentSerializer(documents, many=True)
        response_data = {
            "results": serializer.data,
            "detail": "Documents fetched successfully",
        }

        return Response(response_data, status=status.HTTP_200_OK)