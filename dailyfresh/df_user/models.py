from django.db import models
from db.base_model import BaseModel  # 导入抽象模型基类
from utils.get_hash import get_hash  # 导入sha1加密函数
# Create your models here.


class PassportManager(models.Manager):
    '''账户模型管理器类'''
    def add_one_passport(self, username, password, email):
        '''添加一个用户注册信息'''
        # 1.获取sefl所在模型类
        model_class = self.model
        # 2.创建一个model_class模型类对象
        obj = model_class(username=username, password=get_hash(password), email=email)

        #1.2合并
        # obj = self.model(username=username, password=password, email=email)
        # 3.保存到数据库中
        obj.save()
        # 4.返回obj
        return obj

    def get_one_passport(self, username,password=None):
        '''根据用户名查询账户信息'''
        try:
            #注意password的值 若为空 不能加密　会报NoneType的错误 进行判断
            if password is None:
                # 只根据用户名查找账户信息
                obj = self.get(username=username)
            else:
                obj = self.get(username=username,password=get_hash(password))
        except self.model.DoesNotExist:
            # 查不到
            obj = None
        return obj


class Passport(BaseModel):
    '''账户信息模型类'''
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=40, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱地址')
    objects = PassportManager()  # 自定义模型管理器类对象
    class Meta:
        db_table = 's_user_account'