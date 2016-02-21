from django.conf.urls import patterns, url
from django.views.generic import ListView
from account.models import Account
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from . import views

urlpatterns = [
    url(r'^accueil$', views.home),
    url(r'^statistics$', views.statistics),
    url(r'^release$', views.release),
    url(r'^add$', views.db_add),
    url(r'^update$', views.db_update),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})$', views.month_view),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<category>\w+)$', views.month_view),
    url(r'^modify/(?P<year>\d{4})/(?P<month>\d{2})$', views.db_modify),
    url(r'^modify/nocheck$', views.db_modify),
    url(r'^modify/bymonth$', views.month_choice),
    url(r'^$', RedirectView.as_view(url='accueil'), name='redirect_home'),
]
