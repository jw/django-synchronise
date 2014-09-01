from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt
from synchronise.views import SynchroniseView

urlpatterns = patterns(
    '',
    url(r'^', csrf_exempt(SynchroniseView.as_view()), name='synchronise'),
)