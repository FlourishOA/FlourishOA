from django.test import TestCase
from api.models import Journal, Price
from datetime import date
from pytz import UTC
from api.serializers import JournalSerializer, PriceSerializer
from unittest import skip

"""
Unit tests for the model serializers
"""

class TestJournalSerializer(TestCase):
    """
    Testing behavior of the Journal model serializer
    """
    def setUp(self):
        # note that the data is represented as unicode
        # the numbers are strings, carrying 5 decimal places
        self.j1_query_data = {
            'issn': u'1353-651X',
            'journal_name': u'Journal 1',
            'pub_name': u'Big Pub 1',
            'is_hybrid': False,
            'category': None
        }
        self.j2_query_data = {
            'issn': u'5553-1519',
            'journal_name': u'Journal 2',
            'pub_name': u'Big Pub 2',
            'is_hybrid': False,
            'category': None
        }
        # Normal, valid test case w/no est. art. infl.
        self.j1 = Journal.objects.create(**self.j1_query_data)
        # Journal with no article infl.
        self.j2 = Journal.objects.create(**self.j2_query_data)

    def test_serialize_single(self):
        serializer = JournalSerializer(self.j1)
        self.assertEqual(serializer.data, self.j1_query_data)

        serializer = JournalSerializer(self.j2)
        self.assertEqual(serializer.data, self.j2_query_data)

    def test_serialize_many(self):
        serializer = JournalSerializer(Journal.objects.all(), many=True)
        self.assertEqual([dict(i) for i in serializer.data],
                         [
                             self.j1_query_data,
                             self.j2_query_data,
                         ])


class TestPriceSerializer(TestCase):
    """
    testing behavior of the Price model serializer
    """
    def setUp(self):
        # Unicode formatted data with correct num of decimal places
        self.j1_data = {
            u'issn': u'1353-651X',
            u'journal_name': u'Journal 1',
            u'is_hybrid': False,
            u'category': None
        }
        self.j2_data = {
            u'issn': u'5553-1519',
            u'journal_name': u'Journal 2',
            u'is_hybrid': False,
            u'category': None
        }


        # Normal, valid test case w/no est. art. infl.
        self.j1 = Journal.objects.create(**self.j1_data)

        # Data needed to create price 1 for journal 1
        self.j1p1_create_data = {
            u'journal': self.j1,
            u'price': u'2500.00',
            u'date_stamp': str(date(2010, 10, 25))
        }

        self.j1p1_expected_serialized = {
            u'issn': u'1353-651X',
            u'price': u'2500.00',
            u'date_stamp': str(date(2010, 10, 25))
        }

        # Price with full, down to second time-stamp
        self.j1p1 = Price.objects.create(**self.j1p1_create_data)

    def test_serialize_single(self):
        ser = PriceSerializer(self.j1p1)
        self.assertEqual(self.j1p1_expected_serialized, ser.data)

    def test_deserialize_single(self):
        ser = PriceSerializer(data=self.j1p1_expected_serialized)
        ser.is_valid()
        print ser.errors
        self.assertTrue(ser.is_valid())

