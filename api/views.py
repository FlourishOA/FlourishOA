from .models import Journal
from .serializers import JournalSerializer

from rest_framework import generics
from rest_framework import permissions
from django.contrib.auth.models import User


class JournalList(generics.ListAPIView):
    """
    For accessing the entirety of the journals in the database
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer


class JournalDetail(generics.RetrieveUpdateAPIView):
    """
    For accessing/updating single journals by ISSN
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'issn_number'
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer

