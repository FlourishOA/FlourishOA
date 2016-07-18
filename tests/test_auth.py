from django.test import TestCase
from unittest import skip
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from rest_framework.authtoken import views as auth_views
from rest_framework import serializers
import json


class TestAuthentication(TestCase):

    def setUp(self):
        self.u = User.objects.create_user(username='test1', password='thisis8chars')
        self.u.save()
        self.token = Token.objects.create(user=self.u)
        self.token.save()

    def test_create_valid_request(self):
        # Assertions that should be left regardless
        self.assertEqual(User.objects.get(username='test1'), self.u)
        self.assertEqual(self.u.username, 'test1')

        data = {"username": "test1", "password": "thisis8chars"}
        url = "/api-token-auth/"

        response = self.client.post(url, json.dumps(data), content_type='application/json')
        token = json.loads(response.content)['token']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(token, str(self.token))
