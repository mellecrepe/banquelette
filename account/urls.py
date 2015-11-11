from django.conf.urls import patterns, url
from django.views.generic import ListView
from account.models import Account
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

urlpatterns = patterns('account.views',
    url(r'^accueil$', 'home'),
    url(r'^release$', 'release'),
    url(r'^add$', 'couchdb_add'),
    url(r'^update$', 'couchdb_update'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})$', 'month_view'),
    url(r'^modify/(?P<year>\d{4})/(?P<month>\d{2})$', 'couchdb_modify'),
    url(r'^modify/nocheck$', 'couchdb_modify'),
    url(r'^modify/bymonth$', 'month_choice'),
    url(r'^$', RedirectView.as_view(url='accueil'), name='redirect_home'),
)
