from rest_framework import serializers

from calyvim.models import TeamMembership, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "display_name",
            "avatar"
        ]


class TeamMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TeamMembership
        fields = ["id", "user", "created_at"]


class TeamMembershipCreateSerializer(serializers.Serializer):
    team_id = serializers.UUIDField()
    member_id = serializers.UUIDField()