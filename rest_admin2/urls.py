"""rest_admin2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users.views import UserViewSet, GroupViewSet, SmsCodeViewset
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.authtoken import views

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, base_name='users')
# 配置codes的url
router.register(r'code', SmsCodeViewset, base_name="code")
# router.register(r'groups', GroupViewSet, base_name='groups')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    # 调试登录
    path('api-auth/', include('rest_framework.urls')),
    # drf自带的token授权登录,获取token需要向该地址post数据
    path('login/', obtain_jwt_token),

]