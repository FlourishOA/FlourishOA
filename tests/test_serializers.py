from django.test import TestCase
from api.models import Journal, Publisher, Price
from api.serializers import JournalSerializer, \
                            PriceSerializer, \
                            PublisherSerializer


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
        self.j1_data = {
            'issn': u'1353-651X',
            'journal_name': u'Journal 1',
            'article_influence': u'122.40000',
            'est_article_influence': None,
            'is_hybrid': False,
            'category': None
        }
        self.j2_data = {
            'issn': u'5553-1519',
            'journal_name': u'Journal 2',
            'article_influence': None,
            'est_article_influence': u'15.20000',
            'is_hybrid': False,
            'category': None
        }
        # Normal, valid test case w/no est. art. infl.
        self.j1 = Journal.objects.create(**self.j1_data)
        # Journal with no article infl.
        self.j2 = Journal.objects.create(**self.j2_data)

    def test_serialize_single(self):
        serializer = JournalSerializer(self.j1)
        self.assertEqual(serializer.data, self.j1_data)

        serializer = JournalSerializer(self.j2)
        self.assertEqual(serializer.data, self.j2_data)

    def test_serialize_many(self):
        serializer = JournalSerializer(Journal.objects.all(), many=True)
        self.assertEqual([dict(i) for i in serializer.data],
                         [
                             self.j1_data,
                             self.j2_data,
                         ])


class TestPriceSerializer(TestCase):
    """
    testing behavior of the Price model serializer
    """
    def setUp(self):
        self.j1_data = {
            'issn': '1353-651X',
            'journal_name': 'Journal 1',
            'article_influence': 122.40000,
            'est_article_influence': None,
            'is_hybrid': False,
            'category': None
        }
        self.j2_data = {
            'issn': '5553-1519',
            'journal_name': 'Journal 2',
            'article_influence': None,
            'est_article_influence': 15.2,
            'is_hybrid': False,
            'category': None
        }
        # Normal, valid test case w/no est. art. infl.
        self.j1 = Journal.objects.create(**self.j1_data)
        # Journal with no article infl.
        self.j2 = Journal.objects.create(**self.j2_data)

        # Price with full, down to second time-stamp
        Price.objects.create(journal=self.j1,
                             price=2500,
                             time_stamp='2010-10-25 14:30-07:00')
        # Updated first price, with down to minute time-stamp
        Price.objects.create(journal=self.j1,
                             price=2750,
                             time_stamp='2012-10-28 19:50-07:00')
        # Again update, with variation of down to second time-stamp
        Price.objects.create(journal=self.j1,
                             price=2500,
                             time_stamp='2014-02-12 14:30:26-07:00')
        # Price with just date
        Price.objects.create(journal=self.j2,
                             price=0,
                             time_stamp='2011-12-05 00:00:00-07:00')

    def test_serialize_single(self):
        pass

    def test_serialize_many(self):
        pass


class TestPublisherSerializer(TestCase):
    """
    Test case for the Publisher model serializer
    """

    def setUp(self):
        # Normal, valid test case w/no est. art. infl.
        Journal.objects.create(issn='1353-651X',
                               journal_name='Journal 1',
                               article_influence=122.4,
                               est_article_influence=None,
                               is_hybrid=False,
                               category=None)
        # Journal with no article infl.
        Journal.objects.create(issn='5553-1519',
                               journal_name='Journal 2',
                               article_influence=None,
                               est_article_influence=15.2,
                               is_hybrid=False,
                               category=None)
        j1 = Journal.objects.get(issn='1353-651X')
        j2 = Journal.objects.get(issn='5553-1519')
        Publisher.objects.create(publisher_name='Big Pub 1', journal=j1)
        Publisher.objects.create(publisher_name='Small Pub 1', journal=j2)

    def test_serialize_single(self):
        pass

    def test_serialize_many(self):
        pass
