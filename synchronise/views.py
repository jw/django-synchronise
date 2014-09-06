from django.http import HttpResponse
from django.views.generic import View

from synchronise import synchronise

import json

import logging
logger = logging.getLogger(__name__)


class SynchroniseView(View):

    def post(self, request, *args, **kwargs):
        """
        Handle the synchronise request.  Gets the JSON payload and,
        if available the user name and project name of the GitHub side.
        Then is synchronisation is done.
        """
        try:
            payload_string = request.POST['payload']
            payload_json = json.loads(payload_string)
            user = request.GET.get('user')
            project = request.GET.get('project')
            return synchronise.synchronise(payload_json, user, project)
        except KeyError as ke:
            return HttpResponse("Post contains invalid JSON.\n",
                                status=400)
