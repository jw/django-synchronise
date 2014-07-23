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

    @unittest.skip("The post test still need to use mock objects")
    def test_valid_post(self):
        print("VALID POST?")
        valid_post = {
            'payload': [
                '{"repository": {"website": "", "fork": false, '
                '"name": "hub", "scm": "hg", "owner": "elevenbits", '
                '"absolute_url": "/elevenbits/hub/", "slug": "hub", '
                '"is_private": true}, "truncated": false, "commits": '
                '[{"node": "e7abfeb787b0", "files": [{"type": "modified", '
                '"file": "README.md"}], "raw_author": '
                '"Jan Willems <jw@elevenbits.com>", "utctimestamp": '
                '"2014-07-09 21:04:24+00:00", "author": "elevenbits", '
                '"timestamp": "2014-07-09 23:04:24", "raw_node": '
                '"e7abfeb787b014a87f80d91701ab4a3b74575a32", '
                '"parents": ["2d28ff4f9bd2"], "branch": "default", '
                '"message": "README.md edited online with Bitbucket", '
                '"revision": 10, "size": -1}], "canon_url": '
                '"https://bitbucket.org", "user": "elevenbits"}'
            ]
        }
        #
        #
        #     {
        #     "payload" : {
        #     "user": "elevenbits",
        #     "canon_url": "https://bitbucket.org",
        #     "repository": {
        #         "slug": "hub",
        #         "absolute_url": "/elevenbits/hub/",
        #         "website": "",
        #         "fork": False,
        #         "scm": "hg",
        #         "name": "hub",
        #         "owner": "elevenbits",
        #         "is_private": True
        #     },
        #     "truncated": False,
        #     "commits": [
        #         {
        #             "files": [
        #                 {
        #                     "type": "modified",
        #                     "file": "README.md"
        #                 }
        #             ],
        #             "utctimestamp": "2014-07-05 19:11:06+00:00",
        #             "raw_node": "7031be7915b6ea295c95b6dd9ce35871842127f9",
        #             "timestamp": "2014-07-05 21:11:06",
        #             "parents": ["50be77fba01f"],
        #             "node": "7031be7915b6",
        #             "author": "elevenbits",
        #             "raw_author": "Jan Willems <jw@elevenbits.com>",
        #             "size": -1,
        #             "message": "README.md edited online with Bitbucket",
        #             "revision": 4,
        #             "branch": "default"
        #         }
        #     ]
        # }}
        response = self.client.post('/synchronise/', valid_post)
        print(response.content)
        self.assertEqual(response.status_code, 200)
