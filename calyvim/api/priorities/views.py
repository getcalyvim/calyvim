from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from calyvim.models.priority import Priority
from calyvim.mixins import BoardMixin
from calyvim.api.priorities.serializers import PrioritySerializer, PriorityUpdateSerializer, PriorityCreateSerializer
from calyvim.permissions import BoardGenericPermission
from calyvim.utils import get_object_or_raise_api_404
from calyvim.exceptions import InvalidInputException


class PrioritiesViewSet(BoardMixin, ViewSet):
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
            case "partial_update":
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
        priorities = Priority.objects.filter(board=request.board)
        serializer = PrioritySerializer(priorities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        create_serializer = PriorityCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            raise InvalidInputException
        
        data = create_serializer.validated_data
        priority = Priority.objects.create(board=request.board, **data)
        serializer = PrioritySerializer(priority)
        
        response_data = {
            "detail": "Priority created successfully",
            "priority": serializer.data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):
        priority = get_object_or_raise_api_404(Priority, id=kwargs["pk"], board=request.board)
        update_serializer = PriorityUpdateSerializer(data=request.data)
        if not update_serializer.is_valid():
            raise InvalidInputException
        
        data = update_serializer.validated_data
        for key, value in data.items():
            setattr(priority, key, value)
        
        priority.save(update_fields=data.keys())
        serializer = PrioritySerializer(priority)
        
        response_data = {
            "detail": "Priority data updated successfully",
            "priority": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        priority = get_object_or_raise_api_404(Priority, id=kwargs["pk"], board=request.board)
        priority.delete()
        
        response_data = {
            "detail": "Priority deleted successfully",
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)