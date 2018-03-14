from django.shortcuts import render
from django.views.generic import View

from .models import CourseOrg, CityDict
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        all_citys = CityDict.objects.all()

        # 对城市进行筛选
        city_id = request.GET.get('city_id')
        if city_id:
            all_orgs = all_orgs.filter(city_id=city_id)

        # 对类别进行筛选
        category = request.GET.get('ct')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        # 使用第三方分页器
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)
        return render(request, 'org-list.html', {'orgs':orgs, 
                                                 'all_citys':all_citys, 
                                                 'city_id':city_id, 
                                                 'category':category, 
                                                 'all_orgs':all_orgs, 
                                                 'hot_orgs':hot_orgs,
                                                 'sort':sort,})