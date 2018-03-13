from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic import View
# Create your views here.
from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
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
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')

class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form':register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email')
            # 注册前先检测用户是否已存在
            if UserProfile.objects.filter(email=email):
                return render(request, 'register.html', {'msg':'用户已经存在'})
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

        return render(request, 'register.html', {'register_form':register_form, 'msg':'表单填写出错'})
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
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 将email传回来
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "forgetpwd.html", { "msg": "您的重置密码链接无效,请重新请求"})

    def post(self, request, active_code=None):
        # 将前端表单提交的数据实例化为django_form
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1')
            pwd2 = request.POST.get('password2')
            email = request.POST.get('email')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email':email, 'msg':'密码不一致'})
            else:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(pwd2)  # 修改密码
                user.save()
                return render(request, "login.html")
        else:
            return render(request, 'password_reset.html', {'email':email, 'modify_form':modify_form})