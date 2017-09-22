from django.conf.urls import url
from df_user import views

urlpatterns = [
    url(r'^register/$',views.register),  # 显示注册页面
    url(r'^register_handle/$', views.register_handle),  # 用户注册
]
