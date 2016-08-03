from .models import Journal, Price, Influence
from .serializers import JournalSerializer, PriceSerializer

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
        # if the given ISSN and the ISSN in the new request.data aren't the same
        if not issn or (issn != request.data['issn']):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # creating new Journal model
        journal, journal_created = Journal.objects.update_or_create(
            issn=issn,
            defaults=request.data
        )

        response_data = JournalSerializer(journal).data
        if journal_created:
            return Response(data=response_data, status=status.HTTP_201_CREATED)
        return Response(data=response_data, status=status.HTTP_200_OK)

    def partial_update(self, request, issn=None, *args, **kwargs):
        if (not issn) or (not 'issn' in request.data) or (issn != request.data['issn']):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)

class PriceViewSet(mixins.ListModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'issn'

    def list(self, request, *args, **kwargs):
        queryset = Price.objects.all()
        serializer = PriceSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, issn=None, *args, **kwargs):
        # checking for valid issn and making sure price for given journal at given time doesn't exist
        if (not issn or (request.data['issn'] != issn) or
                Price.objects.filter(journal__issn=issn, date_stamp=request.data['date_stamp']).exists()):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not Journal.objects.filter(issn=issn).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        Price.objects.create(price=request.data['price'],
                             date_stamp=request.data['date_stamp'],
                             journal=Journal.objects.get(issn=request.data['issn']))
        return Response(status=status.HTTP_201_CREATED)

    def retrieve(self, request, issn=None, *args, **kwargs):
        """
        Lists information about journal with given ISSN
        """
        queryset = Price.objects.filter(journal__issn=issn)
        serializer = PriceSerializer(queryset, many=True)
        return Response(serializer.data)


class InfluenceViewSet(mixins.UpdateModelMixin,
                       viewsets.ViewSet):

    permissions = (permissions.IsAuthenticated,)
    lookup_field = 'issn'

    def update(self, request, issn=None, *args, **kwargs):
        if (not issn or (issn not in request.data) or
                Influence.objects.filter(journal__issn=issn, date_stamp=request.data['data_stamp']).exists()):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not Journal.objects.filter(issn=issn).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.data['article_influence'] is None:
            return Response(status=status.HTTP_200_OK)

        Influence.objects.create(article_influence=request.data['article_influence'],
                                 date_stamp=request.data['date_stamp'],
                                 journal=Journal.objects.get(issn=issn))
        return Response(status=status.HTTP_201_CREATED)