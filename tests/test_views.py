from django.test import TestCase
from unittest import skip
from api.models import Journal
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from api.views import JournalViewSet
from django.contrib.auth.models import User
import json

"""
Unit tests for the views
"""


class TestJournalViewSet(TestCase):
    """
    Tests for the JournalViewSet
    """
    def setUp(self):
        """Journal.objects.create(issn='1353-651X',
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
                               category=None)"""
        pass

    def test_journal_viewset_get_list_empty(self):
        factory = APIRequestFactory()
        request = factory.get('journals/')
        view = JournalViewSet.as_view({'get': 'list'})
        response = view(request)
        response.render()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_journal_viewset_get_list_not_empty(self):
        Journal.objects.create(issn='5553-1519',
                               journal_name='Journal 2',
                               article_influence=None,
                               est_article_influence=15.2,
                               is_hybrid=False,
                               category=None)
        correct_data = {
            'issn': '5553-1519',
            'journal_name': 'Journal 2',
            'article_influence': None,
            'est_article_influence': '15.20000',
            'is_hybrid': False,
            'category': None,
        }

        factory = APIRequestFactory()
        request = factory.get('journals/')
        view = JournalViewSet.as_view({'get': 'list'})
        response = view(request)
        response.render()

        self.assertEqual(response.data, [correct_data])

    def test_journal_viewset_get_single_empty(self):
        factory = APIRequestFactory()
        request = factory.get('journals/', {'issn': '5553-1519'})
        view = JournalViewSet.as_view({'get': 'retrieve'})
        response = view(request, issn='5553-1519')
        response.render()

        self.assertEqual(response.status_code, 404)

    def test_journal_viewset_get_single_not_empty(self):
        Journal.objects.create(issn='5553-1519',
                               journal_name='Journal 2',
                               article_influence=None,
                               est_article_influence=15.2,
                               is_hybrid=False,
                               category=None)
        correct_data = {
            'issn': '5553-1519',
            'journal_name': 'Journal 2',
            'article_influence': None,
            'est_article_influence': '15.20000',
            'is_hybrid': False,
            'category': None,
        }

        factory = APIRequestFactory()
        request = factory.get('journals/', {'issn': '5553-1519'})
        view = JournalViewSet.as_view({'get': 'retrieve'})
        response = view(request, issn='5553-1519')
        response.render()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, correct_data)

    """
    Testing the update function of the JournalViewSet
    """

    def test_journal_viewset_update_nonexistent(self):

        user = User.objects.create_user(username='test1', password='passw')

        Journal.objects.create(issn='5553-1519',
                               journal_name='Journal 2',
                               article_influence=None,
                               est_article_influence=15.2,
                               is_hybrid=False,
                               category=None)

        new_data = {
            'issn': '5553-1519',
            'journal_name': 'Journal 27',
            'article_influence': None,
            'est_article_influence': '17.30200',
            'is_hybrid': True,
            'category': None,
        }

        factory = APIRequestFactory()
        request = factory.put('journals/', json.dumps(new_data), content_type='application/json')
        force_authenticate(request, user=user)

        view = JournalViewSet.as_view({'put': 'update'})
        response = view(request, issn='5553-1519')
        response.render()
        print response

    @skip("not implemented yet")
    def test_journal_viewset_update_existent(self):
        pass




