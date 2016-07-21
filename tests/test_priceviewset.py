# General testing
from rest_framework.test import APITestCase
from unittest import skip
from rest_framework.reverse import reverse
import json

# Stuff from my app
from api.models import Price, Journal

# Authentication
from django.contrib.auth.models import User


class TestPriceViewSet(APITestCase):
    def setUp(self):
        self.j1_data = {
            'issn': u'5553-1519',
            'journal_name': u'Journal 2',
            'article_influence': None,
            'est_article_influence': u'15.20000',
            'is_hybrid': False,
            'category': None,
        }

        self.j1p1_data = {
            'price': u'2500.00',
            'time_stamp': u'2016-02-13T10:41:51Z',
            'issn': u'5553-1519'
        }

    def test_get_all_empty(self):
        """
        Checking whether empty list is returned
        """
        response = self.client.get(reverse('price-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    @skip("Unicode issues, needs to be reimplemented")
    def test_get_all_not_empty(self):
        # creating objects
        Journal.objects.create(**self.j1_data)

        response = self.client.get(reverse('price-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual([dict(response.data[0])], [])
