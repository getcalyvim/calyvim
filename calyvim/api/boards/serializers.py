from rest_framework import serializers

from calyvim.mixins import NameAndSourceSerializerMixin
from calyvim.models import User, Board, Task, Label, Priority, State, Sprint, Estimate


class BoardCreateSerializer(serializers.Serializer):
    workspace_id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    template_id = serializers.UUIDField(required=False, allow_null=True)


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["id", "name", "slug", "cover", "logo", "description", "created_at"]


class BoardDetailSerializer(NameAndSourceSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = [
            "id",
            "name",
            "slug",
            "cover",
            "logo",
            "task_prefix",
            "description",
            "created_at",
        ]


class BoardUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    cover = serializers.CharField(required=False, allow_null=True)
    logo = serializers.CharField(required=False, allow_null=True)
    slug = serializers.CharField(required=False)
    task_prefix = serializers.CharField(required=False)
    description = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    current_group_by = serializers.CharField(required=False, allow_null=True)


class BoardMemberSeralizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "display_name",
            "avatar",
        ]


class TaskSerializer(serializers.ModelSerializer):
    board = BoardSerializer()

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "board_id",
            "board",
            "task_type",
            "summary",
            "created_at",
        ]


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ["id", "name", "board_id", "sequence", "category", "created_at"]


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "avatar",
            "display_name",
        ]


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ["id", "name", "created_at"]


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ["id", "name", "color", "created_at"]


class AssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "display_name",
            "last_name",
            "avatar",
        ]


class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ["id", "name", "start_date", "end_date", "is_active", "created_at"]


class EstimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimate
        fields = ["id", "key", "value", "description", "created_at"]
