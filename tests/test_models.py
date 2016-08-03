from django.test import TestCase
from api.models import Journal, Price

"""
Overall testing plan:
    -Unit tests for models
    -Unit tests for views
"""


"""
Unit tests for the models
"""


class TestJournalModel(TestCase):
    """
    Testing behavior of the Journal model
    """
    def setUp(self):
        # Normal, valid test case w/no est. art. infl.
        Journal.objects.create(issn='1353-651X',
                               journal_name='Journal 1',
                               is_hybrid=False,
                               category=None)
        # Journal with no article infl.
        Journal.objects.create(issn='5553-1519',
                               journal_name='Journal 2',
                               is_hybrid=False,
                               category=None)

    def test_journal_str(self):
        j1 = Journal.objects.get(issn='1353-651X')
        j2 = Journal.objects.get(issn='5553-1519')
        self.assertEqual(j1.__str__(),
                         "1353-651X: Journal 1")
        self.assertEqual(j2.__str__(),
                         "5553-1519: Journal 2")


class TestPriceModel(TestCase):
    """
    testing behavior of the Price model
    """
    def setUp(self):
        # Normal, valid test case w/no est. art. infl.
        Journal.objects.create(issn='1353-651X',
                               journal_name='Journal 1',
                               is_hybrid=False,
                               category=None)
        # Journal with no article infl.
        Journal.objects.create(issn='5553-1519',
                               journal_name='Journal 2',
                               is_hybrid=False,
                               category=None)

        j1 = Journal.objects.get(issn='1353-651X')
        j2 = Journal.objects.get(issn='5553-1519')

        # Price with full, down to second time-stamp
        Price.objects.create(journal=j1,
                             price=2500,
                             date_stamp='2010-10-25')
        # Updated first price, with down to minute time-stamp
        Price.objects.create(journal=j1,
                             price=2750,
                             date_stamp='2012-10-28')
        # Again update, with variation of down to second time-stamp
        Price.objects.create(journal=j1,
                             price=2500,
                             date_stamp='2014-02-12')
        # Price with just date
        Price.objects.create(journal=j2,
                             price=0,
                             date_stamp='2011-12-05')

    def test_price_str(self):
        j1 = Journal.objects.get(issn='1353-651X')
        j2 = Journal.objects.get(issn='5553-1519')

        # getting QuerySet of Journal 1's prices
        j1_ps = Price.objects.filter(journal=j1)

        self.assertEqual(j1_ps[0].__str__(), "1353-651X: 2500.00, 2010-10-25;")
        self.assertEqual(j1_ps[1].__str__(), "1353-651X: 2750.00, 2012-10-28;")
        self.assertEqual(j1_ps[2].__str__(), "1353-651X: 2500.00, 2014-02-12;")


        # getting Journal 2's ONLY price
        j2_p = Price.objects.get(journal=j2)
        # Note that Django stores the timezone as UTC
        self.assertEqual(j2_p.__str__(), "5553-1519: 0.00, 2011-12-05;")

