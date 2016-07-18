from django.test import TestCase
from unittest import skip
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from rest_framework.authtoken import views as auth_views
from rest_framework import serializers
import json


class TestAuthentication(TestCase):
    """
    def setUp(self):
        self.u = User.objects.create(username='test1', password='thisis8chars')
        self.token = Token.objects.create(user=self.u)
    """

    def test_create_valid_request(self):
        u = User.objects.create(username='test1', password='thisis8chars')
        Token.objects.create(user=u)
        # Assertions that should be left regardless
        self.assertEqual(User.objects.get(username='test1'), u)
        self.assertEqual(u.username, 'test1')
        self.assertEqual(u.password, 'thisis8chars')

        data = {'username': 'test1', 'password': 'thisis8chars'}
        url = "/api-token-auth/"

        response = self.client.post(url, data)
        print response.status_code
        print response.content
        """
        request = APIRequestFactory().post("/api-token-auth/",
                                           data={'username': 'test1', 'password': 'thisis8chars'}, format='json')
        print request.body
        view = auth_views.ObtainAuthToken.as_view()

        response = view(request)
        response.render()

        print response.content

        """