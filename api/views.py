from .models import Journal, Price, Publisher
from .serializers import JournalSerializer, PriceSerializer, PublisherSerializer

from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import json


class JournalViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'issn'

    def list(self, request, *args, **kwargs):
        """
        Lists information about journals
        """
        queryset = Journal.objects.all()
        serializer = JournalSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, issn=None, *args, **kwargs):
        """
        Lists information about journal with given ISSN
        """
        queryset = Journal.objects.all()
        journal = get_object_or_404(queryset, issn=issn)
        serializer = JournalSerializer(journal)
        return Response(serializer.data)

    def update(self, request, issn=None, *args, **kwargs):
        """
        Updates/creates information about journal with given ISSN
        """
        try:
            json_data = json.loads(request.data)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # if the given ISSN and the ISSN in the new json_data aren't the same
        if issn != json_data['issn']:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        journal, created = Journal.objects.update_or_create(issn=issn, defaults=json_data)
        if created:
            return Response(data=JournalSerializer(journal).data, status=status.HTTP_201_CREATED)
        return Response(JournalSerializer(journal).data)

    def partial_update(self, request, issn=None, *args, **kwargs):
        """
        Updates only fields that differ between request and stored data
        """
        journal = get_object_or_404(Journal.objects.all(), issn=issn)
        ser = JournalSerializer(journal, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PriceViewSet(mixins.ListModelMixin,
                   viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'journal'

    def list(self, request, journal=None, *args, **kwargs):
        if journal:
            queryset = Price.objects.filter(journal=journal)
        else:
            queryset = Price.objects.all()
        serializer = PriceSerializer(queryset, many=True)
        return Response(serializer.data)

