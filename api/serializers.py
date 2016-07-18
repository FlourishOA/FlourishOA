from rest_framework import serializers
from .models import Journal, Price, Publisher
from django.contrib.auth.models import User


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        write_only_fields = ('password',)


class JournalSerializer(serializers.ModelSerializer):
    """
    Allows Journal model to be serialized into JSON/other formats for
    use by the REST API
    """
    class Meta:
        model = Journal
        fields = ('issn', 'journal_name', 'article_influence', 'est_article_influence',
                  'is_hybrid', 'category')


class PriceSerializer(serializers.ModelSerializer):
    """
    Allows Price model to be serialized into JSON/other formats for
    use by the REST API
    """
    class Meta:
        model = Price
        fields = ('price', 'time_stamp', 'journal')


class PublisherSerializer(serializers.ModelSerializer):
    """
    Allows Publisher model to be serialized into JSON/other formats for
    use by the REST API
    """
    class Meta:
        model = Publisher
        fields = ('publisher_name', 'journal')
