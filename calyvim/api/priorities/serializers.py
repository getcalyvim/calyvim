from rest_framework import serializers

from calyvim.models.priority import Priority


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ["id", "board_id", "name", "created_at"]


class PriorityUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=False)


class PriorityCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)