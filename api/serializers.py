from rest_framework import serializers
from .models import Journal, Price
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        write_only_fields = ('password',)


class JournalSerializer(serializers.ModelSerializer):
    """
    Allows Journal model to be serialized into JSON/other formats for
    use by the REST API
    """
    # TODO: fix the journal/issn conflict
    class Meta:
        model = Journal
        fields = ('issn', 'journal_name', 'pub_name', 'article_influence', 'est_article_influence',
                  'is_hybrid', 'category')


class PriceSerializer(serializers.ModelSerializer):
    """
    Allows Price model to be serialized into JSON/other formats for
    use by the REST API
    """
    issn = serializers.ReadOnlyField(source='journal.issn', read_only=True)

    class Meta:
        model = Price
        fields = ('price', 'time_stamp', 'issn')

