from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from calyvim.models import Block, Document
from calyvim.mixins import DocumentMixin
from calyvim.api.blocks.serializers import BlockSerializer


class BlocksViewst(DocumentMixin, ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        page_id = request.query_params.get("page_id", None)

        blocks = Block.objects.filter(document=request.document, page_id=page_id)
        serializer = BlockSerializer(blocks, many=True)

        response_data = {
            "results": serializer.data,
            "detail": "Blocks fetched successfully",
        }
        return Response(data=response_data, status=200)

    @action(detail=False, methods=["POST"])
    def operations(self, request, *args, **kwargs):
        print(request.data)
        return Response(data={}, status = 200)
        # page_id = request.query_params.get("page_id", None)

        # blocks = Block.objects.filter(document=request.document, page_id=page_id)
        # serializer = BlockSerializer(blocks, many=True)

        # response_data = {
        #     "results": serializer.data,
        #     "detail": "Blocks fetched successfully",
        # }
        # return Response(data=response_data, status=200)
