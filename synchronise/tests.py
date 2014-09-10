from django.test import Client
from urllib.parse import quote_plus

import unittest

import synchronise


class VersionTest(unittest.TestCase):

    def test_version_plain(self):
        self.assertEqual(synchronise.get_version(), '0.2.0')

    def test_version_short(self):
        self.assertEqual(synchronise.get_version(), '0.2.0')


class BitBucketToGitHubTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_empty_post(self):
        response = self.client.post('/synchronise/', {})
        self.assertEqual(response.status_code, 400)

    def test_empty_post_with_user(self):
        response = self.client.post('/synchronise/?user=jw', {})
        self.assertEqual(response.status_code, 400)

    def test_invalid_json_posts(self):
        content_type = 'application/x-www-form-urlencoded'
        # prepare the first request (no JSON payload)
        invalid_json = '{ "Hello": "There" }'
        invalid_json_url = quote_plus(invalid_json)
        payload = b'payload=' + bytes(invalid_json_url, 'utf-8')
        # send it off
        response = self.client.post('/synchronise/?user=jw',
                                    payload, content_type=content_type)
        # check
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.reason_phrase, 'No proper JSON in payload.')
        # prepare the second request (invalid JSON payload)
        invalid_json = '{ "Invalid": "No empty quote }'
        invalid_json_url = quote_plus(invalid_json)
        payload = b'payload=' + bytes(invalid_json_url, 'utf-8')
        # send it off
        response = self.client.post('/synchronise/?user=jw',
                                    payload, content_type=content_type)
        # check
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.reason_phrase, 'Invalid JSON payload.')

    def test_valid_post1(self):
        """
        Test the push of this repository to the same repository on GitHub.
        """
        valid_post = {
            'payload': '{                                        '
                       '   "canon_url": "https://bitbucket.org", '
                       '   "repository": {                       '
                       '       "scm": "hg",                      '
                       '       "owner": "elevenbits",            '
                       '       "name": "django-synchroniser"     '
                       '   },                                    '
                       '   "user": "elevenbits"                  '
                       '}                                        '
        }
        response = self.client.post('/synchronise/',
                                    valid_post)
        self.assertEqual(response.status_code, 200)

    def test_valid_post2(self):
        """
        Test the push of this repository to the same repository on GitHub.
        """
        valid_post = {
            'payload': '{                                        '
                       '   "canon_url": "https://bitbucket.org", '
                       '   "repository": {                       '
                       '       "scm": "hg",                      '
                       '       "owner": "elevenbits",            '
                       '       "name": "django-synchroniser"     '
                       '   },                                    '
                       '   "user": "elevenbits"                  '
                       '}                                        '
        }
        user_project = 'user=jw&project=django-synchronise'
        response = self.client.post('/synchronise/?' + user_project,
                                    valid_post)
        self.assertEqual(response.status_code, 200)
