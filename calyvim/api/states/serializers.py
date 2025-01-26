from rest_framework import serializers

from calyvim.models import State


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ["id", "name", "description", "sequence", "category", "created_at"]


class StateSequenceUpdateSerializer(serializers.Serializer):
    previous_state = serializers.UUIDField(required=False)
    next_state = serializers.UUIDField(required=False)


class StateCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )


class StateUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    category = serializers.ChoiceField(required=False, choices=State.Category.choices)
