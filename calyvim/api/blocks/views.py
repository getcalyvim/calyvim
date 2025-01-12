from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db import transaction
from django.utils import timezone

from calyvim.models import Block, Document
from calyvim.mixins import DocumentMixin
from calyvim.api.blocks.serializers import BlockSerializer, OperationsSerializer


class BlocksViewst(DocumentMixin, ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        page_id = request.query_params.get("page_id", None)

        # Fetch the content list from the document
        content_order = request.document.content

        blocks = Block.objects.filter(document=request.document, page_id=page_id)

        # Sort the blocks based on the order in the content list
        sorted_blocks = sorted(blocks, key=lambda block: content_order.index(block.id))

        serializer = BlockSerializer(sorted_blocks, many=True)

        response_data = {
            "results": serializer.data,
            "detail": "Blocks fetched successfully",
        }
        return Response(data=response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    @transaction.atomic
    def operations(self, request, *args, **kwargs):
        serializer = OperationsSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                data={
                    "detail": "Failed to perform update operations",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = serializer.validated_data
        original_content = request.document.content
        blocks_to_remove = set(original_content) - set(data["content"])

        for block_id, values in data["updates"].items():
            block = Block.objects.filter(id=block_id, document=request.document).first()

            if not block:
                block = Block.objects.create(
                    id=block_id,
                    document=request.document,
                    properties={},
                    created_by=request.user,
                )
            for key, value in values.items():
                setattr(block, key, value)
            block.save(update_fields=values.keys())

            request.document.content = data["content"]
            request.document.save(update_fields=["content"])

        if len(blocks_to_remove) > 0:
            block_ids = list(blocks_to_remove)
            Block.objects.filter(id__in=block_ids, document=request.document).update(
                is_archived=True, archived_at=timezone.now()
            )

        response_data = {
            "detail": "Blocks updated successfully",
        }
        return Response(data=response_data, status=status.HTTP_200_OK)
