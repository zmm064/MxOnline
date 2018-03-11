from datetime import datetime

from django.db import models

from users.models import UserProfile
from courses.models import Course

class UserAsk(models.Model):
    '''用户咨询'''
    name           = models.CharField('姓名', max_length=20)
    moblie         = models.CharField('手机号', max_length=11)
    course_name    = models.CharField('课程名', max_length=50)
    add_time       = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name


class CourseComment(models.Model):
    '''课程评论'''
    user   = models.ForeignKey(UserProfile, verbose_name='用户')
    course = models.ForeignKey(Course, verbose_name='课程')

    comments = models.CharField('评论', max_length=200)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    '''用户收藏'''
    TYPE_CHOICES = (
        (1, u'课程'),
        (2, u'课程机构'),
        (3, u'讲师')
    )

    user = models.ForeignKey(UserProfile, verbose_name='用户')

    # 从特定的收藏类型中进行筛选
    fav_type = models.IntegerField('收藏类型', choices=TYPE_CHOICES, default=1)
    fav_id = models.IntegerField(default=0)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    '''用户消息'''
    # 为0发给所有用户，不为0就是发给用户的id
    user = models.IntegerField('接收用户', default=0)
    message = models.CharField('消息内容', max_length=500)
    has_read = models.BooleanField('是否已读', default=False)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    '''用户课程'''
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    course = models.ForeignKey(Course, verbose_name='课程')

    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name