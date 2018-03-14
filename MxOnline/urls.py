"""
Definition of urls for MxOnline.
"""

import xadmin
from xadmin.plugins import xversion
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.views.static import serve

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
xadmin.autodiscover()
xversion.register_models()
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView
from organization.views import OrgView
from MxOnline.settings import MEDIA_ROOT

urlpatterns = [
    # Examples:
    # url(r'^$', MxOnline.views.home, name='home'),
    # url(r'^MxOnline/', include('MxOnline.MxOnline.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'xadmin/', include(xadmin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='useractive'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^org-list/$', OrgView.as_view(), name='org-list'),
    

    # 配置静态文件的处理服务器
    url(r'media/(?P<path>.*)/$', serve, {'document_root':MEDIA_ROOT}),
]
