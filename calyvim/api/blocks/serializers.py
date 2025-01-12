from rest_framework import serializers

from calyvim.models import Block


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = [
            "id",
            "page_id",
            "block_type",
            "content",
            "properties",
            "created_at",
        ]