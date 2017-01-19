from .models import Journal, Price, Influence
from .serializers import JournalSerializer, PriceSerializer, InfluenceSerializer

from rest_framework import permissions, status, viewsets, mixins
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.views import APIView
from rest_framework import response, schemas


class SchemaView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    renderer_classes = [SwaggerUIRenderer, OpenAPIRenderer]

    def get(self, request):
        generator = schemas.SchemaGenerator(title='PriceSleuth API')
        return response.Response(generator.get_schema(request=request))


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
        if not issn or ('issn' in request.data and issn != request.data['issn']):
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
        # must have ISSN, year; Price with same date and journal must not already exist;
        # given ISSN must match given data; either ArticleInfluence or est. ArticleInfluence must be non-null
        if (not issn or ('issn' not in request.data) or
                (request.data['issn'] != issn) or ('date_stamp' not in request.data) or
                (request.data['price'] is None) or (request.data['price'] < 0) or
                Price.objects.filter(journal__issn=issn, date_stamp=request.data['date_stamp']).exists()):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # journal with relevant ISSN must already exist
        if not Journal.objects.filter(issn=issn).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            influence = Influence.objects.get(journal__issn=issn,
                                              date_stamp__year=request.data['date_stamp'][0:4])
        except Influence.DoesNotExist:
            influence = None
        Price.objects.create(price=request.data['price'],
                             date_stamp=request.data['date_stamp'],
                             journal=Journal.objects.get(issn=issn),
                             influence=influence)

        return Response(status=status.HTTP_201_CREATED)

    def retrieve(self, request, issn=None, *args, **kwargs):
        """
        Lists information about journal with given ISSN
        """
        queryset = Price.objects.filter(journal__issn=issn)
        serializer = PriceSerializer(queryset, many=True)
        return Response(serializer.data)


class InfluenceViewSet(mixins.UpdateModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.ViewSet):

    # Write-only, so authentication is always required
    permissions = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'issn'

    def update(self, request, issn=None, *args, **kwargs):
        # must have ISSN, year; Influence with same year and journal must not already exist;
        # given ISSN must match given data; either ArticleInfluence or est. ArticleInfluence must be non-null
        if (not issn or ('issn' not in request.data) or
                ('issn' in request.data and request.data['issn'] != issn) or ('year' not in request.data) or
                Influence.objects.filter(journal__issn=issn, date_stamp__year=request.data['year']).exists() or
                (request.data['article_influence'] is None and request.data['est_article_influence'] is None)):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # journal with relevant ISSN must already exist
        if not Journal.objects.filter(issn=issn).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        # deciding whether to use est. ArticleInfluence or regular ArticleInfluence
        if request.data['article_influence'] is not None:
            Influence.objects.create(article_influence=request.data['article_influence'],
                                     date_stamp=request.data['year'] + "-12-31",
                                     journal=Journal.objects.get(issn=issn))
        else: # est. ArticleInfluence must not be none then
            Influence.objects.create(est_article_influence=request.data['est_article_influence'],
                                     date_stamp=request.data['year'] + "-12-31",
                                     journal=Journal.objects.get(issn=issn))

        return Response(status=status.HTTP_201_CREATED)

    def retrieve(self, request, issn=None, *args, **kwargs):
        queryset = Influence.objects.filter(journal__issn=issn)
        serializer = InfluenceSerializer(queryset, many=True)
        return Response(serializer.data)

