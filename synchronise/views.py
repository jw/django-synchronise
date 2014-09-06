from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

from synchronise import synchronise

import json


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
            user = request.GET['user']
            project = request.GET['project']
            return synchronise.handle_post(payload_json, user, project)
        except KeyError as ke:
            return HttpResponse("Post contains invalid JSON.\n",
                                status=400)
