from django.conf.urls import patterns, url
from django.views.generic import ListView
from account.models import Account
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

urlpatterns = patterns('account.views',
    url(r'^accueil$', 'home'),
    url(r'^release$', 'release'),
    url(r'^add$', 'db_add'),
    url(r'^update$', 'db_update'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})$', 'month_view'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<category>\w+)$', 'month_view'),
    url(r'^modify/(?P<year>\d{4})/(?P<month>\d{2})$', 'db_modify'),
    url(r'^modify/nocheck$', 'db_modify'),
    url(r'^modify/bymonth$', 'month_choice'),
    url(r'^$', RedirectView.as_view(url='accueil'), name='redirect_home'),
)
