from django.shortcuts import render
from .serializers import UserMobileRegSerializers, UserDetailSerializers, GroupSerializers, SmsSerializer
from rest_framework import mixins, permissions, authentication
from rest_framework import viewsets, status
from django.contrib.auth import get_user_model
Users = get_user_model()
from django.contrib.auth.models import Group
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework.response import Response
from random import choice
from utils.miaodisms import MiaoDiSMS
from .models import VerifyCode
from django.contrib.auth.backends import ModelBackend
# Create your views here.


class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码字符串
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]

        miao_di = MiaoDiSMS()

        code = self.generate_code()

        sms_status = miao_di.send_sms(code=code, mobile=mobile)

        if sms_status["respCode"] == "00000":
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "mobile": sms_status["respDesc"]
            }, status=status.HTTP_400_BAD_REQUEST)


class AdminViewSet(viewsets.ModelViewSet):
    serializer_class = []
    queryset = Users.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_admin:
            return 1
        return 2


class UserViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = []
    queryset = Users.objects.all()
    lookup_field = "mobile"
    authentication_classes = (JSONWebTokenAuthentication,  authentication.SessionAuthentication)

    def get_serializer_class(self):
        if self.action == "create":
            return UserMobileRegSerializers
        return UserDetailSerializers

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = self.perform_create(serializer)
    #
    #     re_dict = serializer.data
    #     payload = jwt_payload_handler(user)
    #     re_dict["token"] = jwt_encode_handler(payload)
    #     re_dict["name"] = user.name if user.name else user.username
    #
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 重写该方法，不管传什么id，都只返回当前用户
    # def get_object(self):
    #     user = self.request.user
    #     print(user)
    #     return self.request.user

    def perform_create(self, serializer):
        return serializer.save()

class GroupViewSet():
    serializer_class = GroupSerializers
    queryset = Group.objects.all()