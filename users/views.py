from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
# Create your views here.
from .models import UserProfile


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # username或者为邮箱或者为用户名
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                print("登录成功！")
                return user
        except Exception as e:
            return None

def user_login(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        # 此处将调用我们自己定义的认证方法
        user = authenticate(username=user_name, password=pass_word)
        if user:
            login(request, user)
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {'msg':'用户名或密码错误！'})
    elif request.method == 'GET':
        return render(request, 'login.html')
