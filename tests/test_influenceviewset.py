# General testing
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
import json

# Stuff from my app
from api.models import Influence, Journal
from api.serializers import InfluenceSerializer
# Authentication
from django.contrib.auth.models import User


class TestInfluenceViewSet(APITestCase):
    def setUp(self):
        self.j1_data = {
            'issn': u'5553-1519',
            'journal_name': u'Journal 2',
            'is_hybrid': False,
            'category': None,
        }

        self.j2_data = {
            'issn': '1234-1519',
            'journal_name': 'Weird Bad Journal',
            'is_hybrid': True,
            'category': None,

        }

        self.j1i1_request_data = {
            'article_influence': u'0.5871000',
            'est_article_influence': None,
            'date_stamp': u'2016-02-13',
            'issn': u'5553-1519',
        }

    def test_get_all_empty(self):
        response = self.client.get(reverse('influence-detail', kwargs={'issn': '5553-1519'}))
        self.assertEqual(response.status_code, 401)

        user = User.objects.create_user(username='test1', password='passw')
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse('influence-detail', kwargs={'issn': '5553-1519'}))
        self.assertEqual(response.status_code, 405)

    """
    Testing the update function of the PriceViewSet
    """
    def test_update_nonexistent(self):
        Journal.objects.create(**self.j1_data)

        # setting up user and info to be update
        user = User.objects.create_user(username='test1', password='passw')
        self.client.force_authenticate(user=user)

        # rendering the changes into the Django view (and by proxy, the model)
        response = self.client.put(reverse('influence-detail', kwargs={'issn': '5553-1519'}),
                                   data=self.j1i1_request_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(InfluenceSerializer(Influence.objects.get(journal__issn='5553-1519')).data,
                         self.j1i1_request_data)

