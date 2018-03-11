from datetime import datetime

from django.db import models

class Course(models.Model):
    '''课程基本信息'''
    DEGREE_CHOICES = (
        ('cj', '初级'),
        ('zj', '中级'),
        ('gj', '高级'),
    )

    name        = models.CharField('课程名', max_length=50)
    desc        = models.CharField('课程描述', max_length=300)
    detail      = models.TextField('课程详情')
    degree      = models.CharField('难度', choices=DEGREE_CHOICES, max_length=2)
    learn_times = models.IntegerField('学习时长（分钟）', default=0)    
    students    = models.IntegerField('学习人数', default=0)
    fav_nums    = models.IntegerField('收藏人数', default=0)
    image       = models.ImageField('封面图', upload_to='courses/%Y/%m')
    click_nums  = models.IntegerField('点击数' ,default=0)
    add_time    = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Lesson(models.Model):
    '''课程下的章节'''
    course   = models.ForeignKey(Course, verbose_name='课程')

    name     = models.CharField('章节名', max_length=50)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name


class Video(models.Model):
    '''课程章节下的视频'''
    lesson   = models.ForeignKey(Lesson, verbose_name='章节')

    name     = models.CharField('视频名', max_length=50)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

class CourseResource(models.Model):
    '''课程下的相关资源'''
    course   = models.ForeignKey(Course, verbose_name='课程')

    name     = models.CharField('课程名称', max_length=50)
    download = models.FileField(upload_to='courses/resource/%Y/%m')
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name