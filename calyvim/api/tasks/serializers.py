from rest_framework import serializers

from calyvim.models import (
    Task,
    User,
    Priority,
    Label,
    TaskComment,
    Estimate,
    Sprint,
    State,
)


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ["id", "name", "board_id", "sequence", "created_at"]


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


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ["id", "name", "color"]


class CreatedBySerializer(serializers.ModelSerializer):
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


class QuerySerializer(serializers.Serializer):
    assignees = serializers.ListField(child=serializers.UUIDField(), required=False)


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ["id", "name", "created_at"]


class EstimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimate
        fields = ["id", "key", "value"]


class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ["id", "name", "start_date", "end_date", "is_active", "created_at"]


class TaskCreateSerializer(serializers.Serializer):
    summary = serializers.CharField()
    description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    task_type = serializers.ChoiceField(choices=Task.TaskType.choices)
    state_id = serializers.UUIDField()
    priority_id = serializers.UUIDField(required=False, allow_null=True)
    # assignees = serializers.ListField(
    #     child=serializers.UUIDField(), required=False, allow_empty=True
    # )
    assignee_id = serializers.UUIDField(required=False, allow_null=True)
    parent_id = serializers.UUIDField(required=False)
    sprint_id = serializers.UUIDField(required=False, allow_null=True)

class TaskSerializer(serializers.ModelSerializer):
    assignees = AssigneeSerializer(many=True)
    labels = LabelSerializer(many=True)
    priority = PrioritySerializer()
    estimate = EstimateSerializer()
    sprint = SprintSerializer()
    created_by = CreatedBySerializer()
    assignee_ids = serializers.SerializerMethodField()
    label_ids = serializers.SerializerMethodField()
    task_type_display = serializers.SerializerMethodField()
    assignee = AssigneeSerializer()

    class Meta:
        model = Task
        fields = [
            "id",
            "parent_id",
            "state_id",
            "priority_id",
            "sprint_id",
            "sprint",
            "task_type",
            "task_type_display",
            "number",
            "name",
            "summary",
            "description",
            "sequence",
            "assignee",
            "assignee_id",
            "assignees",
            "assignee_ids",
            "labels",
            "label_ids",
            "priority",
            "estimate_id",
            "estimate",
            "links",
            "checklists",
            "created_by",
            "created_at",
        ]

    def get_assignee_ids(self, obj):
        return list(map(lambda x: x.id, obj.assignees.all()))

    def get_label_ids(self, obj):
        return list(map(lambda x: x.id, obj.labels.all()))

    def get_task_type_display(self, obj):
        return obj.get_task_type_display()


class TaskSequenceUpdateSerializer(serializers.Serializer):
    previous_task = serializers.UUIDField(required=False)
    state_id = serializers.UUIDField()
    next_task = serializers.UUIDField(required=False)


class TaskUpdateSerializer(serializers.Serializer):
    summary = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    assignee_ids = serializers.ListField(
        child=serializers.UUIDField(), allow_empty=True, required=False
    )
    priority_id = serializers.UUIDField(required=False, allow_null=True)
    state_id = serializers.UUIDField(required=False)
    task_type = serializers.ChoiceField(choices=Task.TaskType, required=False)
    estimate_id = serializers.UUIDField(required=False)
    sprint_id = serializers.UUIDField(required=False, allow_null=True)
    assignee_id = serializers.UUIDField(required=False, allow_null=True)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "display_name",
            "last_name",
            "avatar",
        ]


class TaskCommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = TaskComment
        fields = ["id", "content", "author", "comment_type", "created_at"]
