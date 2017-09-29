
from django.conf.urls import url

from df_cart import views

urlpatterns = [
    url(r'^add/$', views.cart_add), # 添加商品到购物车
    url(r'^count/$', views.cart_count),  # 获取购物车中的商品的总数
]
