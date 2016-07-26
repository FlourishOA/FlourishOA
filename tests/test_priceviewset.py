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
        # TODO: rewrite this data to reflect new schema
        self.j1_data = {
            'issn': u'5553-1519',
            'journal_name': u'Journal 2',
            'article_influence': None,
            'est_article_influence': u'15.20000',
            'is_hybrid': False,
            'category': None,
        }

        self.j2_data = {
            'issn': '1234-1519',
            'journal_name': 'Weird Bad Journal',
            'article_influence': None,
            'est_article_influence': '1.20010',
            'is_hybrid': True,
            'category': None,

        }

        self.j1p1_request_data = {
            'price': u'2500.00',
            'time_stamp': u'2016-02-13T10:41:51Z',
            'issn': u'5553-1519',
        }



    def test_get_all_empty(self):
        # TODO: finish test
        pass

    def test_get_all_not_empty(self):
        # TODO: finish test
        pass

    """
    Testing the update function of the PriceViewSet
    """
    def test_update_nonexistent(self):
        Journal.objects.create(**self.j1_data)

        response = self.client.get(reverse('price-detail', kwargs={'issn': '5553-1519'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

        # setting up user and info to be update
        user = User.objects.create_user(username='test1', password='passw')
        self.client.force_authenticate(user=user)

        # rendering the changes into the Django view (and by proxy, the model)
        response = self.client.put(reverse('price-detail', kwargs={'issn': '5553-1519'}),
                                   data=self.j1p1_request_data, format='json')
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('price-detail', kwargs={'issn': '5553-1519'}))

        # data received should be the same as the original dict
        self.assertEqual(response.status_code, 200)
        self.assertEqual([dict(response.data[0])], [self.j1p1_request_data])

    def test_update_existent(self):
        # TODO: finish test
        pass

    def test_non_uniform_issn_update(self):
        # TODO: finish test
        pass

    def test_no_auth_update(self):
        # TODO: finish test
        pass