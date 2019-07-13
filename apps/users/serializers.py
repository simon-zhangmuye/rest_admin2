# coding=utf-8
__author__ = 'Simon Zhang'
__date__ = '2018/12/11 11:45'

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import VerifyCode
from datetime import datetime, timedelta
import re
from rest_admin2.settings import REGEX_MOBILE
User = get_user_model()

class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码(函数名称必须为validate_ + 字段名)
        """
        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        # 添加时间大于一分钟以前。也就是距离现在还不足一分钟
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile




class UserDetailSerializers(ModelSerializer):
    """
    用户详情序列化
    """
    id = serializers.IntegerField(read_only=True, label="ID", help_text="ID")
    class Meta:
        model = User
        fields = ("id","name","gender","birthday","email")



class UserMobileRegSerializers(ModelSerializer):
    id = serializers.IntegerField(read_only=True, label="ID", help_text="ID")
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text="验证码")
    mobile = serializers.CharField(max_length=11, min_length=11, required=True, label="电话",
                                   help_text="电话",allow_blank=False,
                                   error_messages={
                                       "blank": "请输入手机号",
                                       "required": "请输入手机号",
                                       "max_length": "手机号格式错误",
                                       "min_length": "手机号格式错误"
                                   },
                                   validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    password = serializers.CharField(max_length=100, required=True, label="密码")

    # 调用父类的create方法，该方法会返回当前model的实例化对象即user。
    # 前面是将父类原有的create进行执行，后面是加入自己的逻辑
    def create(self, validated_data):
        user = super(UserMobileRegSerializers, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def validated_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["mobile"]).order_by("-add_time")
        if verify_records:
            # 获取到最新一条
            last_record = verify_records[0]

            # 有效期为五分钟。
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

# 不加字段名的验证器作用于所有字段之上。attrs是字段 validate之后返回的总的dict
    def validate(self, attrs):
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ('id','mobile','code','password')

class GroupSerializers(ModelSerializer):
    class Meta:
        model = Group
        fields = ('id','mobile','code','password')