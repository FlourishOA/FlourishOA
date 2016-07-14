from django.test import TestCase
from api.models import Journal, Publisher, Price

"""
Overall testing plan:
    -Unit tests for models
    -Unit tests for views
"""


"""
Unit tests for the models
"""
class JournalModelTestCase(TestCase):
    """
    Testing behavior of the Journal model
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

    def test_journal_str(self):
        j1 = Journal.objects.get(issn='1353-651X')
        j2 = Journal.objects.get(issn='5553-1519')
        self.assertEqual(j1.__str__(),
                         "1353-651X: Journal 1")
        self.assertEqual(j2.__str__(),
                         "5553-1519: Journal 2")


class PriceModelTestCase(TestCase):
    """
    testing behavior of the Price model
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

        # Price with full, down to second time-stamp
        Price.objects.create(journal=j1,
                             price=2500,
                             time_stamp='2010-10-25 14:30-07:00')
        # Updated first price, with down to minute time-stamp
        Price.objects.create(journal=j1,
                             price=2750,
                             time_stamp='2012-10-28 19:50-07:00')
        # Again update, with variation of down to second time-stamp
        Price.objects.create(journal=j1,
                             price=2500,
                             time_stamp='2014-02-12 14:30:26-07:00')
        # Price with just date
        Price.objects.create(journal=j2,
                             price=0,
                             time_stamp='2011-12-05 00:00:00-07:00')

    def test_price_str(self):
        j1 = Journal.objects.get(issn='1353-651X')
        j2 = Journal.objects.get(issn='5553-1519')

        # getting QuerySet of Journal 1's prices
        j1_ps = Price.objects.filter(journal=j1)

        self.assertEqual(j1_ps[0].__str__(), "1353-651X: 2500.00, 2010-10-25 21:30:00+00:00;")
        self.assertEqual(j1_ps[1].__str__(), "1353-651X: 2750.00, 2012-10-29 02:50:00+00:00;")
        self.assertEqual(j1_ps[2].__str__(), "1353-651X: 2500.00, 2014-02-12 21:30:26+00:00;")


        # getting Journal 2's ONLY price
        j2_p = Price.objects.get(journal=j2)
        # Note that Django stores the timezone as UTC
        self.assertEqual(j2_p.__str__(), "5553-1519: 0.00, 2011-12-05 07:00:00+00:00;")


class PublisherModelTestCase(TestCase):
    """
    Test case for the Publisher model
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

    def test_publisher_str(self):
        big_pub = Publisher.objects.get(publisher_name='Big Pub 1')
        small_pub = Publisher.objects.get(publisher_name='Small Pub 1')

        self.assertEqual(big_pub.__str__(), 'Big Pub 1: 1353-651X')
        self.assertEqual(small_pub.__str__(), 'Small Pub 1: 5553-1519')
