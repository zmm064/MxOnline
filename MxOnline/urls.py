"""
Definition of urls for MxOnline.
"""

import xadmin
from xadmin.plugins import xversion
from django.conf.urls import include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
xadmin.autodiscover()
xversion.register_models()

urlpatterns = [
    # Examples:
    # url(r'^$', MxOnline.views.home, name='home'),
    # url(r'^MxOnline/', include('MxOnline.MxOnline.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'xadmin/', include(xadmin.site.urls)),
]

# version模块自动注册需要版本控制的 Model
