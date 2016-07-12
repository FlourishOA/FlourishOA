from .models import Journal
from .serializers import JournalSerializer

from rest_framework import generics
from rest_framework import permissions
from django.contrib.auth.models import User


class JournalList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer


class JournalDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'issn_number'
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer

