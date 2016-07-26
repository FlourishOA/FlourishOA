# General testing
from rest_framework.test import APITestCase
from unittest import skip
from rest_framework.reverse import reverse
import json

# Stuff from my app
from api.models import Journal

# Authentication
from django.contrib.auth.models import User


"""
Unit tests for the views
"""


class TestJournalViewSet(APITestCase):
    """
    Tests for the JournalViewSet
    """
    def setUp(self):
        self.journal1_data = {
            'issn': u'5553-1519',
            'journal_name': u'Journal 2',
            'pub_name': u'Publisher 1',
            'article_influence': None,
            'est_article_influence': u'15.20000',
            'is_hybrid': False,
            'category': None,
        }
        self.updated_journal1_data = {
            'issn': u'5553-1519',
            'journal_name': u'Journal 27',
            'pub_name': u'Publisher 2',
            'article_influence': None,
            'est_article_influence': u'17.30200',
            'is_hybrid': True,
            'category': None,
        }

        self.journal2_data = {
            'issn': u'1234-1519',
            'journal_name': u'Weird Bad Journal',
            'pub_name': u'Publisher 2',
            'article_influence': None,
            'est_article_influence': u'1.20010',
            'is_hybrid': True,
            'category': None,
        }

    def test_get_list_empty(self):
        """
        Checking whether empty list is returned
        """
        response = self.client.get(reverse('journal-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_get_list_not_empty(self):
        # creating objects
        Journal.objects.create(**{i: self.journal1_data[i] for i in self.journal1_data if i != 'pub_name'})
        response = self.client.get(reverse('journal-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [dict(response.data[0])],
            [{i: self.journal1_data[i] for i in self.journal1_data if i != 'pub_name'}]
        )

    def test_get_single_empty(self):
        response = self.client.get(reverse('journal-detail', kwargs={'issn': '5553-1519'}))
        self.assertEqual(response.status_code, 404)

    def test_get_single_not_empty(self):
        # creating objects
        Journal.objects.create(**{i: self.journal1_data[i] for i in self.journal1_data if i != 'pub_name'})
        response = self.client.get(reverse('journal-detail', kwargs={'issn': '5553-1519'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            dict(response.data),
            {i: self.journal1_data[i] for i in self.journal1_data if i != 'pub_name'}
        )

    """
    Testing the update function of the JournalViewSet
    """
    def test_update_nonexistent(self):

        response = self.client.get(reverse('journal-detail', kwargs={'issn': '5553-1519'}))
        self.assertEqual(response.status_code, 404)

        # setting up user and info to be update
        user = User.objects.create_user(username='test1', password='passw')
        self.client.force_authenticate(user=user)

        # rendering the changes into the Django view (and by proxy, the model)
        response = self.client.put(reverse('journal-detail', kwargs={'issn': '5553-1519'}),
                                   data=self.journal1_data, format='json')
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('journal-detail', kwargs={'issn': '5553-1519'}))

        # data received should be the same as the original dict
        self.assertEqual(response.status_code, 200)
        # TODO: fix this, possibly modify the models
        #self.assertEqual(response.data, self.journal1_data)

    def test_update_existent(self):

        # creating journal so there is something in the database
        Journal.objects.create(**{i: self.journal1_data[i] for i in self.journal1_data if i != 'pub_name'})

        response = self.client.get(reverse('journal-detail', kwargs={'issn': '5553-1519'}))

        # data received should be the same as the original dict
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {i: self.journal1_data[i] for i in self.journal1_data if i != 'pub_name'}
        )

        # setting up user and info to be update
        user = User.objects.create_user(username='test1', password='passw')
        self.client.force_authenticate(user=user)

        # rendering the changes into the Django view (and by proxy, the model)
        tmp = reverse('journal-detail', kwargs={'issn': '5553-1519'}),
        response = self.client.put(reverse('journal-detail', kwargs={'issn': '5553-1519'}),
                                   data=self.updated_journal1_data, format='json')
        self.assertEqual(response.status_code, 200)

        # data retrieved should be the same as the data we had before
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            self.updated_journal1_data,
        )

    def test_non_uniform_issn_update(self):
        # creating journal so there is something in the database
        Journal.objects.create(**{i: self.journal1_data[i] for i in self.journal1_data if i != 'pub_name'})

        # setting up user and authenticating
        user = User.objects.create_user(username='test1', password='passw')
        self.client.force_authenticate(user=user)

        # sending the ISSN for journal1, but having a different ISSN in the data
        response = self.client.put(reverse('journal-detail', kwargs={'issn': '5553-1519'}),
                                   data=self.journal2_data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_no_auth_update(self):
        # trying to update data with no authenication, should result in 'Unauthorized'
        # response from the server
        response = self.client.put(reverse('journal-detail', kwargs={'issn': '5553-1519'}),
                                   data=json.dumps(self.journal1_data), format='json')
        self.assertEqual(response.status_code, 401)





