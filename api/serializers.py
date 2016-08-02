from rest_framework import serializers
from .models import Journal, Price, Publisher, Type, Influence, Category
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
    class Meta:
        model = Journal
        fields = ('issn', 'journal_name')


class DateStampedSerializer(serializers.ModelSerializer):
    issn = serializers.ReadOnlyField(source='journal.issn', read_only=True)


class PriceSerializer(DateStampedSerializer):
    """
    Allows Price model to be serialized into JSON/other formats for
    use by the REST API
    """
    class Meta:
        model = Price
        fields = ('price', 'date_stamp', 'issn')


class PublisherSerializer(DateStampedSerializer):
    class Meta:
        model = Publisher
        fields = ('pub_name', 'date_stamp', 'issn')


class InfluenceSerializer(DateStampedSerializer):
    class Meta:
        model = Influence
        fields = ('article_influence', 'est_article_influence', 'date_stamp', 'issn')


class TypeSerializer(DateStampedSerializer):
    class Meta:
        model = Type
        fields = ('is_hybrid', 'date_stamp', 'issn')


class CategorySerializer(DateStampedSerializer):
    class Meta:
        model = Category
        fields = ('category', 'date_stamp', 'issn')