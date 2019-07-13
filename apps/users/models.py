from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.contrib import admin
from datetime import datetime
# Create your models here.
class UserProfile(AbstractUser):
    """用户表"""
    gender_choice = (("male","男"),("female","女"))
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name="用户", help_text="用户", unique=True)
    gender = models.CharField(choices=gender_choice, max_length=6, default="male", verbose_name="性别", help_text="性别")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月", help_text="出生年月")
    mobile = models.CharField(max_length=11, unique=True, null=False, blank=False, verbose_name="电话", help_text="电话")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class Group(Group):
    pass



class VerifyCode(models.Model):
    """
    短信验证码,回填验证码进行验证
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "短信验证"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
