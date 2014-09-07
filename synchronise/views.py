from django.http import HttpResponse
from django.views.generic import View

from synchronise import synchronise

import json

import logging
logger = logging.getLogger(__name__)


class SynchroniseView(View):

    def post(self, request, *args, **kwargs):
        """
        Handle the synchronise request.  Gets the JSON payload and check
        for the user name and project name.  Then the synchroniser is called.
        """
        try:
            payload_string = request.POST['payload']
            payload_json = json.loads(payload_string)
            user = request.GET.get('user')
            project = request.GET.get('project')
            return synchronise.synchronise(payload_json, user, project)
        except ValueError:
            return HttpResponse("Post contains an invalid JSON payload.\n",
                                status=400)
        except KeyError:
            return HttpResponse("A JSON payload needs to be provided.\n",
                                status=400)
