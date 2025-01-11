from calyvim.models import Document, User
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "display_name",
            "email",
            "avatar",
            "username",
        ]


class DocumentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Document
        fields = [
            "id",
            "name",
            "author",
            "description",
            "created_at"
        ]