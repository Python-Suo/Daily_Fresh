# 商品索引类GoodIndex
from haystack import indexes
from df_goods.models import Goods  # 导入模型类


# 索引类的名字: 模型类名+Index
class GoodsIndex(indexes.Indexable, indexes.SearchIndex):
    '''商品索引类'''
    text = indexes.CharField(document=True, use_template=True)  # use_template=True 说明随后要建立一个文件　在这个文件里写入要根据哪些字段生成索引

    def get_model(self):
        # 返回模型类
        return Goods

    def index_queryset(self, using=None):
        return self.get_model().objects.all()