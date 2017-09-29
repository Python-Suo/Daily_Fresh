from django.shortcuts import render
from django.http import JsonResponse
from utils.decorators import login_required
from django.views.decorators.http import require_GET,require_http_methods,require_POST
from df_cart.models import Cart
# Create your views here.


#/cart/add/
@require_GET
@login_required
def cart_add(request):
    '''添加商品到购物车'''
    # 1.获取商品id和商品数目
    goods_id = request.GET.get('goods_id')
    goods_count = request.GET.get('goods_count')
    passport_id = request.session.get('passport_id')
    print(goods_count)
    goods_count = int(goods_count)
    # 2.添加商品到购物车
    res = Cart.objects.add_one_cart_info(goods_id=goods_id,passport_id=passport_id,goods_count=goods_count)
    # 3.判断存储结果
    if res:
        # 添加成功
        return JsonResponse({'res':1})
    else:
        # 添加失败
        return JsonResponse({'res':0})


#/cart/count
@require_GET
@login_required
def cart_count(request):
    '''获取登录用户的购物车商品总数'''
    # 1.获取登录账户id
    passport_id = request.session.get('passport_id')
    # 2.根据passport_id查询用户购物车中商品的总数
    res = Cart.objects.get_cart_count_by_passport(passport_id=passport_id)
    # 3.返回json
    return JsonResponse({'res':res})