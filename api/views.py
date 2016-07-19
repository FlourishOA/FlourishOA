from .models import Journal, Price, Publisher
from .serializers import JournalSerializer, PriceSerializer, PublisherSerializer

from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class JournalViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def list(self, request, *args, **kwargs):
        queryset = Journal.objects.all()
        serializer = JournalSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, issn=None, *args, **kwargs):
        queryset = Journal.objects.all()
        journal = get_object_or_404(queryset, issn=issn)
        serializer = JournalSerializer(journal)
        return Response(serializer.data)

    def update(self, request, issn=None, *args, **kwargs):
        journal, created = Journal.objects.update_or_create(issn=issn, defaults=request.data)
        serializer = JournalSerializer(journal)
        journal.save()

