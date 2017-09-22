from django.db import models
from db.base_model import BaseModel  # 导入抽象模型基类
# Create your models here.


class PassportManager(models.Manager):
    '''账户模型管理器类'''
    def add_one_passport(self, username, password, email):
        '''添加一个用户注册信息'''
        # 1.获取sefl所在模型类
        model_class = self.model
        # 2.创建一个model_class模型类对象
        obj = model_class(username=username, password=password, email=email)

        #1.2合并
        # obj = self.model(username=username, password=password, email=email)
        # 3.保存到数据库中
        obj.save()
        # 4.返回obj
        return obj



class Passport(BaseModel):
    '''账户信息模型类'''
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=40, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱地址')
    objects = PassportManager()  # 自定义模型管理器类对象
    class Meta:
        db_table = 's_user_account'