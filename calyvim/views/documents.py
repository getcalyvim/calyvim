from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin

from calyvim.models import Document
from calyvim.serializers import DocumentSerializer, WorkspaceSerializer


class DocumentDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        document = get_object_or_404(Document, id=kwargs.get("document_id"))

        context = {
            "props": {
                "document": DocumentSerializer(document).data,
                "workspace": WorkspaceSerializer(document.workspace).data,
            }
        }
        return render(request, "documents/detail.html", context)