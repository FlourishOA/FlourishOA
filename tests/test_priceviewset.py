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
            'issn': '5553-1519',
            'journal_name': 'Journal 2',
            'article_influence': None,
            'est_article_influence': '15.20000',
            'is_hybrid': False,
            'category': None,
        }

        self.j1p1_data = {
            'price': 2500,
            'time_stamp': '2016-2-13 10:41:51',
            'journal': '5553-1519'
        }


    def test_get_list_empty(self):
        """
        Checking whether empty list is returned
        """
        response = self.client.get(reverse('price-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])


    def test_get_list_not_empty(self):
        # creating objects
        Journal.objects.create(**self.j1_data)
        Price.objects.create({key: Journal.objects.get(issn=self.j1p1_data['issn']) if key == 'journal' else value
                              for (key, value) in self.j1p1_data})
        response = self.client.get(reverse('price-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [self.j1p1_data])
