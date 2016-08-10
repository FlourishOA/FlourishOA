from rest_framework import serializers

from .models import Journal, Price, Influence
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        write_only_fields = ('password',)


class JournalSerializer(serializers.ModelSerializer):

    # TODO: fix the journal/issn conflict
    class Meta:
        model = Journal
        fields = ('issn', 'journal_name', 'pub_name', 'is_hybrid', 'category')


class PriceSerializer(serializers.ModelSerializer):
    issn = serializers.ReadOnlyField(source='journal.issn', read_only=True)

    class Meta:
        model = Price
        fields = ('price', 'date_stamp', 'issn')


class InfluenceSerializer(serializers.ModelSerializer):
    issn = serializers.ReadOnlyField(source='journal.issn', read_only=True)
    year = serializers.StringRelatedField(source='date_stamp.year', read_only=True)

    class Meta:
        model = Influence
        fields = ('article_influence', 'est_article_influence', 'year', 'issn')
