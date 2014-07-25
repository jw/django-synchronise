from django.test import Client

import unittest
import synchronise


class VersionTest(unittest.TestCase):

    def test_version_plain(self):
        self.assertTrue(synchronise.get_version(), '0.1.0b42')

    def test_version_short(self):
        self.assertTrue(synchronise.get_version(), '0.1.0')


class BBToGHTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_empty_post(self):
        response = self.client.post('/synchronise/', {})
        self.assertEqual(response.status_code, 400)

    def test_invalid_json_posts(self):
        response = self.client.post('/synchronise/',
                                    '{ "invalid": "json" }',
                                    content_type="text/plain")
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/synchronise/',
                                    '{ "invalid": "json }',
                                    content_type="text/plain")
        self.assertEqual(response.status_code, 400)

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
        response = self.client.post('/synchronise/', valid_post)
        self.assertEqual(response.status_code, 200)
