from rest_framework import serializers
from .models import Journal
from django.contrib.auth.models import User


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ('issn_number', 'journal_name', 'article_influence', 'est_article_influence',
                  'is_hybrid', 'category')
