from django.conf.urls import url
from df_user import views

urlpatterns = [
    url(r'^register/$',views.register),  # 显示注册页面
    url(r'^check_user_exist/$', views.check_user_exist),  # 注册重名校验
    # url(r'^register_handle/$', views.register_handle),  # 用户注册处理
    url(r'^login/$', views.login),  # 显示登录界面
    url(r'^login_check/',views.login_check),  # 登录校验
]
