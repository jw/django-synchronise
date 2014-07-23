from django.conf.urls import patterns, url, include
from synchronise.views import SynchroniseView

urlpatterns = patterns(
    '',
    url(r'^', SynchroniseView.as_view(), name='synchronise'),
)
