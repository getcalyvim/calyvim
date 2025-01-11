from calyvim.views.documents import DocumentDetailView
from django.urls import path

urlpatterns = [
    path("", DocumentDetailView.as_view(), name="document-detail"),
]