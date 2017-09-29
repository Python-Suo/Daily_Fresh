from django.db import models
from db.base_manager import BaseManager
from db.base_model import BaseModel
from django.db.models import Sum # 导入聚合类
from df_goods.models import Goods
# Create your models here.


class CartManager(BaseManager):
    '''购物车模型类管理器类'''
    def get_one_cart_info(self, passport_id, goods_id):
        '''判断用户购物车中是否添加过该商品'''
        cart_info = self.get_one_object(passport_id=passport_id, goods_id=goods_id)
        return cart_info

    def add_one_cart_info(self,passport_id,goods_id,goods_count):
        '''添加商品到购物车'''
        cart_info = self.get_one_cart_info(passport_id=passport_id,goods_id=goods_id)
        # 获取该商品具体信息查看其库存
        goods = Goods.objects.get_goods_by_id(gid=goods_id)
        if cart_info:
            # 1.若用户购物车中添加过该商品　更新商品数量
            total_count = cart_info.goods_count + goods_count
            # 判断商品库存是否充足
            if total_count <= goods.goods_stock:
                # 库存充足
                cart_info.goods_count = total_count
                cart_info.save()
                return True
            else:
                # 库存不足
                return False
        else:
            # 2.若购物车中没有添加过该商品,创建新纪录
            # 判断商品库存
            if goods_count <= goods.goods_stock:
                # 库存充足
                self.create_one_object(passport_id=passport_id,goods_id=goods_id,goods_count=goods_count)
                return True
            else:
                # 库存不足
                return False

    def get_cart_count_by_passport(self, passport_id):
        '''获取登录用户购物车中的商品总数'''
        res_dict = self.filter(passport_id=passport_id).aggregate(Sum('goods_count'))
        # {'goods_count__sum':值} 购物车中有商品
        # {'goods_count__sum':None}  购物车中无商品
        # 获取购物车中商品的总数
        res = res_dict.get('goods_count__sum')
        if res is None:
            res = 1
        return res

class Cart(BaseModel):
    '''购物车模型类'''
    passport = models.ForeignKey('df_user.Passport', verbose_name='账户')
    goods = models.ForeignKey('df_goods.Goods', verbose_name='商品')
    goods_count = models.IntegerField(default=0, verbose_name='商品数目')

    objects = CartManager()

    class Meta:
        db_table = 's_cart'