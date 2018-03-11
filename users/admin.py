import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner


class BaseSettings:
    '''设置允许更换主题样式'''
    enable_themes = True
    use_bootswatch = True

class GlobalSettings:
    '''设置首页内容和菜单栏'''
    site_title = '慕学后台管理系统'
    site_footer = '慕学在线网'
    menu_style = 'accordion'

class EmailVerifyRecordAdmin:
    list_display  = ['code', 'email', 'sendtype', 'sendtime']
    list_filter   = ['code', 'email', 'sendtype', 'sendtime']
    search_fields = ['code', 'email', 'sendtype']

class BannerAdmin:
    list_display  = ['title', 'image', 'url', 'index', 'add_time']
    list_filter   = ['title', 'image', 'url', 'index']
    search_fields = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)