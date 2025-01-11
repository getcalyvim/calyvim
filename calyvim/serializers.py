from rest_framework import serializers

from calyvim.mixins import NameAndSourceSerializerMixin
from calyvim.models import Workspace, User, Team, Board, Sprint, Task, Document


class ProfileSerializer(NameAndSourceSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "display_name",
            "avatar",
        ]


class WorkspaceSerializer(NameAndSourceSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = [
            "id",
            "name",
            "slug",
            "logo",
            "description",
            "created_at",
        ]


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name", "created_at"]


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = [
            "id",
            "name",
            "slug",
            "cover",
            "logo",
            "description",
            "is_estimate_enabled",
            "created_at",
            "current_group_by",
        ]


class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ["id", "name", "start_date", "end_date", "is_active", "created_at"]



class MinimalTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "number",
            "created_at"
        ]


class DocumentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()

    class Meta:
        model = Document
        fields = [
            "id",
            "name",
            "author",
            "created_at",
        ]
