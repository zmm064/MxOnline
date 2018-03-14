from django.conf.urls import include, url
from .views import OrgView, AddUserAskView

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name='list'),
    url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask'),

]
