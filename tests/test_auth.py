from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import json


class TestAuthentication(TestCase):

    def setUp(self):
        """
        Creating user and valid token
        """
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

        response = self.client.post(url, data)
        # parsing out the token from the string
        token = json.loads(response.content)['token']

        # checking for valid response status AND the correct token
        self.assertEqual(response.status_code, 200)
        self.assertEqual(token, str(self.token))

    def test_create_invalid_request(self):
        data = {"username": "test1", "password": "thisis9chars"}
        url = "/api-token-auth/"

        response = self.client.post(url, data)

        # bad password should result in bad credentials error
        self.assertEqual(response.status_code, 400)

    def test_full_auth(self):
        data = {"username": "test1", "password": "thisis8chars"}
        url = "/api-token-auth/"

        response = self.client.post(url, data)
        token = json.loads(response.content)['token']