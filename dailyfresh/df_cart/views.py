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
    print(passport_id)
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


# /cart/
@login_required
def cart_show(request):
    '''显示购物车页面'''
    # 1.获取登录用户的passport_id
    passport_id = request.session['passport_id']
    # 2.获取用户的购物车记录信息
    cart_list = Cart.objects.get_cart_list_by_passport(passport_id=passport_id)
    return render(request, 'df_cart/cart.html', {'cart_list':cart_list})


# /cart/update/?goods_id=goods_id&goods_count=goods_count
@require_GET
@login_required
def cart_update(request):
    '''更新购物车数据表中商品的数目'''
    # 1.获取商品的id和商品的数目
    goods_id = request.GET.get('goods_id')
    goods_count = request.GET.get('goods_count')
    passport_id = request.session.get('passport_id')
    # 2.更新用户购物车中的商品的数目
    res = Cart.objects.update_one_cart_info(passport_id=passport_id,goods_id=goods_id,goods_count=int(goods_count))
    # 3.判断res返回的json数据
    if res:
        # 更新成功
        return JsonResponse({'res':1})
    # 更新失败
    return JsonResponse({'res':0})


# /cart/del/?goods_id=商品id
@require_GET
@login_required
def cart_del(request):
    '''删除购物车中商品的记录'''
    # 1.获取商品id
    goods_id = request.GET.get('goods_id')
    passport_id = request.session.get('passport_id')
    # 2.山粗购物车中对应的记录
    res = Cart.objects.del_one_cart_info(passport_id=passport_id,goods_id=goods_id)
    # 3.判断res返回的数据
    if res:
        # 删除成功
        return JsonResponse({'res':1})
    # 删除失败
    return JsonResponse({'res':0})


















