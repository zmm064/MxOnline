from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser  # 继承django现有的用户表


class UserProfile(AbstractUser):
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
    )

    nick_name = models.CharField('昵称', max_length=50, default='')
    birthday  = models.DateField('生日', null=True, blank=True)
    gender    = models.CharField('性别', choices=GENDER_CHOICES, max_length=7)
    address   = models.CharField('地址', max_length=100)
    mobile    = models.CharField(max_length=11, null=True, blank=True)
    image     = models.ImageField(upload_to='image/%Y/%m', default='image/default.png')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    '''发送邮箱验证码'''
    SEND_TYPE_CHOICES = (
        ('register', '注册'),
        ('forget', '找回密码'),
    )

    code     = models.CharField('验证码', max_length=20)
    email    = models.EmailField('邮箱', max_length=50)
    sendtype = models.CharField('验证码类型', choices=SEND_TYPE_CHOICES, max_length=10)
    sendtime = models.DateTimeField('发送时间', default=datetime.now)
    # 默认值可以为可调用对象，这会在类实例化时生成对应的值

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.code}({self.email})'


class Banner(models.Model):
    '''首页轮播图'''
    title    = models.CharField('标题', max_length=100)
    image    = models.ImageField('轮播图', upload_to='banner/%Y/%M')
    url      = models.URLField('访问地址', max_length=200)
    index    = models.IntegerField('轮播图顺序', default=100)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name