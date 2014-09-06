from django.http import HttpResponse
from django.views.generic import View

from synchronise import synchronise

import json

import logging
logger = logging.getLogger(__name__)


class SynchroniseView(View):

    def post(self, request, *args, **kwargs):
        """
        Handle the synchronise request.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            payload_string = request.POST['payload']
            payload_json = json.loads(payload_string)
            user = request.GET.get('user')
            project = request.GET.get('project')
            return synchronise.handle_post(payload_json, user, project)
        except KeyError as ke:
            return HttpResponse("Post contains invalid JSON.\n",
                                status=400)
