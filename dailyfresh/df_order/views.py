from django.shortcuts import render
from django.db import transaction
from df_order.models import OrderBasic,OrderDetail
from df_cart.models import Cart
from df_user.models import Address
from utils.decorators import login_required
from django.views.decorators.http import require_GET,require_http_methods,require_POST
from django.http import JsonResponse
from datetime import datetime
# Create your views here.

# /order/place/
@require_POST
@login_required
def order_place(request):
    '''显示提交订单页面'''
    cart_id_list = request.POST.getlist('cart_id_list')
    # print(cart_id_list)
    # 查询id在cart_id_list中的购物车商品记录
    cart_list = Cart.objects.get_cart_list_by_id_list(cart_id_list=cart_id_list)
    # 获取用户的默认收货地址
    passport_id = request.session.get('passport_id')
    addr = Address.objects.get_one_address(passport_id=passport_id)
    # 把cart_id_list转化成字符串
    cart_id_list = ','.join(cart_id_list)
    return render(request, 'df_order/place_order.html', {'cart_list':cart_list,'addr':addr,'cart_id_list':cart_id_list})


# /order/commit/
@require_POST
@login_required
@transaction.atomic
def order_commit(request):
    '''订单生成'''
    # 接收信息
    addr_id = request.POST.get('addr_id')
    pay_method = request.POST.get('pay_method')
    cart_id_list = request.POST.get('cart_id_list')
    # 获取passport_id
    passport_id = request.session.get('passport_id')
    # 组织订单基本信息数据
    # order_id  20170929143121+passport_id 订单id
    order_id = datetime.now().strftime('%Y%m%d%H%M%S')+str(passport_id)
    # 获取商品运费
    transit_price = 10
    # 计算商品的总数目和总价格
    cart_id_list = cart_id_list.split(',')
    # print(cart_id_list)
    total_count,total_price = Cart.objects.get_amount_and_count_by_id_list(cart_id_list)

    # 设置一个保存点
    sid = transaction.savepoint()
    try:
        # 添加订单基本信息记录
        OrderBasic.objects.add_one_basic_info(order_id=order_id,passport_id=passport_id,addr_id=addr_id,total_count=total_count, total_price=total_price, transit_price=transit_price, pay_method=pay_method)

        # 添加订单详细信息记录
        cart_list = Cart.objects.get_cart_list_by_id_list(cart_id_list=cart_id_list)
        for cart_info in cart_list:
            # 组织订单详细记录数据
            goods_id = cart_info.goods_id
            goods_count = cart_info.goods_count
            # print(goods_count)
            goods_price = cart_info.goods.goods_price
            # 判断商品的库存是否充足
            if goods_count <= cart_info.goods.goods_stock:
                # 库存充足
                # 添加详情记录
                OrderDetail.objects.add_one_detail_info(order_id=order_id, goods_id=goods_id, goods_count=goods_count,goods_price=goods_price)
                # 更新商品表中该商品的库存量和销量
                cart_info.goods.goods_stock = cart_info.goods.goods_stock - goods_count
                cart_info.goods.goods_sales = cart_info.goods.goods_sales + goods_count
                cart_info.goods.save()
                # 删除购物车中对应记录
                cart_info.delete()
            else:
                # 库存不足
                transaction.savepoint_rollback(sid)
                return JsonResponse({'res':0})
    except Exception as e:
        # 发生异常
        print(e)
        transaction.savepoint_rollback(sid)
        return JsonResponse({'res':2})
    # 订单生成成功
    transaction.savepoint_commit(sid)
    return JsonResponse({'res':1})



























