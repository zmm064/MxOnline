from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic import View
# Create your views here.
from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm
from utils.email_send import send_register_email


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


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():  # 加入表单初步验证环节
            user_name = request.POST.get('username')
            pass_word = request.POST.get('password')
            # 此处将调用我们自己定义的认证方法
            user = authenticate(username=user_name, password=pass_word)
            if user:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg':'用户未激活！', 'login_form':login_form})

        return render(request, 'login.html', {'msg':'用户名或密码错误！', 'login_form':login_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for records in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        return render(request, 'login.html')

class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form':register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email')
            pass_word = request.POST.get('password')
            user_profile = UserProfile()
            user_profile.username = email
            user_profile.email = email
            user_profile.is_active = False
            # 保存加密后的密码
            user_profile.password = make_password(pass_word) 
            # 很多该有的字段没有，但也可以，考虑到 model validation is not used by default.
            user_profile.save()
            send_register_email(email, 'register')

        return render(request, 'register.html', {'register_form':register_form})
#def user_login(request):
#    if request.method == 'POST':
#        user_name = request.POST.get('username')
#        pass_word = request.POST.get('password')
#        # 此处将调用我们自己定义的认证方法
#        user = authenticate(username=user_name, password=pass_word)
#        if user:
#            login(request, user)
#            return render(request, 'index.html')
#        else:
#            return render(request, 'login.html', {'msg':'用户名或密码错误！'})
#    elif request.method == 'GET':
#        return render(request, 'login.html')
