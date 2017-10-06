from django.db import models
from db.base_model import BaseModel  # 导入抽象模型基类
from utils.get_hash import get_hash  # 导入sha1加密函数
from db.base_manager import BaseManager # 导入抽象管理器基类
# Create your models here.


class PassportManager(BaseManager):
    '''账户模型管理器类'''
    def add_one_passport(self, username, password, email):
        '''添加一个用户注册信息'''
        # # 1.获取sefl所在模型类
        # model_class = self.model
        # # 2.创建一个model_class模型类对象
        # obj = model_class(username=username, password=get_hash(password), email=email)
        #
        # #1.2合并
        # # obj = self.model(username=username, password=password, email=email)
        # # 3.保存到数据库中
        # obj.save()
        obj = self.create_one_object(username=username, password=get_hash(password), email=email)
        # 4.返回obj
        return obj

    # def get_one_object(self, **view_kwargs):
    def get_one_passport(self, username,password=None):
        '''根据用户名查询账户信息'''
        # try:
        #     #注意password的值 若为空 不能加密　会报NoneType的错误 进行判断
        #     if password is None:
        #         # 只根据用户名查找账户信息
        #         obj = self.get(username=username)
        #     else:
        #         obj = self.get(username=username,password=get_hash(password))
        # except self.model.DoesNotExist:
        #     # 查不到
        #     obj = None
        if password == None:
            obj = self.get_one_object(username=username)
        else:
            obj = self.get_one_object(username=username,password=get_hash(password))
        return obj


class Passport(BaseModel):
    '''账户信息模型类'''
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=40, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱地址')
    objects = PassportManager()  # 自定义模型管理器类对象
    class Meta:
        db_table = 's_user_account'


class AddressManager(BaseManager):
    '''地址模型类管理器类'''
    def get_one_address(self, passport_id):
        '''查询账户的默认收货地址'''
        # try:
        #     addr = self.get(passport_id=passport_id, is_default=True)
        # except self.model.DoesNotExist:
        #     addr = None

        addr = self.get_one_object(passport_id=passport_id, is_default=True)
        return addr

    def add_one_address(self, passport_id, recipient_name, recipient_addr, recipient_phone, zip_code):
        '''添加一个收货地址'''
        # # 查询是否有默认地址
        # addr = self.get_one_address(passport_id=passport_id)
        # # 获取self所在的模型类
        # model_class = self.model
        # if addr is None:
        #     # 1.没有默认收货地址
        #     # 创建一个模型类的对象
        #     # print('测试１')
        #     addr = model_class(passport_id=passport_id, recipient_name=recipient_name,recipient_addr=recipient_addr,recipient_phone=recipient_phone,zip_code=zip_code, is_default=True)
        # else:
        #     # 2.如果已经存在默认收货地址
        #     addr = model_class(passport_id=passport_id, recipient_name=recipient_name, recipient_addr=recipient_addr, recipient_phone=recipient_phone, zip_code=zip_code)
        # # 3.保存数据到数据库中
        # addr.save()

        addr = self.get_one_address(passport_id=passport_id)
        is_default = False
        if addr is None:
            # 1.没有默认地址
            is_default = True
        addr = self.create_one_object(passport_id=passport_id, recipient_name=recipient_name, recipient_addr=recipient_addr, recipient_phone=recipient_phone, zip_code=zip_code,is_default=is_default)
        # 4.返回addr
        return addr


class Address(BaseModel):
    '''用户地址模型类'''
    passport = models.ForeignKey('Passport', verbose_name='所属账户')
    recipient_name = models.CharField(max_length=24, verbose_name='收件人')
    recipient_addr = models.CharField(max_length=256, verbose_name='收件地址')
    recipient_phone = models.CharField(max_length=11, verbose_name='收件电话')
    zip_code = models.CharField(max_length=6, verbose_name='邮政编码')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')
    objects = AddressManager()

    class Meta:
        db_table = 's_user_address'


class BrowseHistoryManager(BaseManager):
    '''历史浏览模型管理器类'''
    def get_one_history(self, passport_id, goods_id):
        '''查询用户是否浏览过某个商品'''
        browsed = self.get_one_object(passport_id=passport_id,goods_id=goods_id)
        return browsed

    def add_one_history(self, passport_id, goods_id):
        '''添加用户的一条浏览记录'''
        # 1.取查找用户是否浏览过该商品
        browsed = self.get_one_history(passport_id=passport_id,goods_id=goods_id)
        # 2.如果用户浏览过该商品,则更新update_time,否则插入一条新的浏览记录,更新update_time在使用save()方法时自动更新
        if browsed:
            # 调用browsed.save()方法会自动更新update_time
            browsed.save()
        else:
            browsed = self.create_one_object(passport_id=passport_id,goods_id=goods_id)
        return browsed

    def get_browse_list_by_passport(self, passport_id, limit=None):
        '''根据passport_id获取对应用户的浏览记录'''
        # 1.根据用户id获取用户的历史浏览记录,browsed_li为一个查询集
        browsed_li = self.get_object_list(filters={'passport_id':passport_id},order_by=('-update_time',))
        # 2.对查询结果进行限制
        if limit:
            browsed_li = browsed_li[:limit]
        return browsed_li


class BrowseHistory(BaseModel):
    '''历史浏览模型类'''
    passport = models.ForeignKey('df_user.Passport', verbose_name='账户')
    goods = models.ForeignKey('df_goods.Goods', verbose_name='商品')

    objects = BrowseHistoryManager()

    class Meta:
        db_table = 's_browse_history'





























