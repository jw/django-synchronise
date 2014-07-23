from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

from synchronise import synchronise

import json


GIT_OWNER = 'jw'


class SynchroniseView(View):

    def is_bitbucket_hg_post(self, post):
        result = False
        if 'bitbucket' in post['canon_url']:
            print("Looks like a Bitbucket repository.")
            repo = post['repository']
            if repo['scm'] == 'hg':
                print("Is a Mercurial repository.")
                result = True
        return result

    def handle_post(self, post):
        if self.is_bitbucket_hg_post(post):
            repo = post['repository']
            # hg_path should be ssh://hg@bitbucket.org/<name>/<project>,
            hg_path = "ssh://hg@bitbucket.org/{}/{}".format(repo['owner'],
                                                            repo['name'])
            # git_path should be git+ssh://git@github.com/<user>/<project>.git
            git_path = "git+ssh://git@github.com/{}/{}.git".format(
                GIT_OWNER, repo['name']
            )
            try:
                synchronise.hg_to_git(hg_path, git_path)
            except hgapi.HgException as he:
                HttpResponse("Could not convert: {}.".format(he),
                             status=409)
        else:
            HttpResponse("Not a valid post. Discarding it.", status=409)
        return HttpResponse('POST: {}\n'.format(post), status=200)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            payload = request.POST['payload']
            post = json.loads(payload)
            return self.handle_post(post)
        except KeyError as ke:
            return HttpResponse("Post contains invalid JSON.\n",
                                status=400)
