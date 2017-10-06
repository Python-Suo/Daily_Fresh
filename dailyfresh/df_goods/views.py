from django.shortcuts import render
from df_goods.models import Goods,Image
from df_goods.enums import *
from django.core.paginator import Paginator  # 导入分页类
from df_user.models import BrowseHistory

# Create your views here.
# 127.0.0.1:8000
def home_list_page(request):
    '''显示首页'''
    # 注意goods_type_id 为SmallIntegerField类型的数据 其中设置了choice属性 取值时可以用　FRUIT或对应的enums文件中FRUIT对应的数字
    # 1.查询水果的4个商品 和　3个新品
    fruits = Goods.objects.get_goods_by_type(goods_type_id=FRUIT, limit=4)
    fruits_new = Goods.objects.get_goods_by_type(goods_type_id=1, limit=3, sort='new')

    # 2.查询海鲜的4个商品 和　3个新品
    seafoods = Goods.objects.get_goods_by_type(goods_type_id=SEAFOOD, limit=4)
    seafoods_new = Goods.objects.get_goods_by_type(goods_type_id=2, limit=3, sort='new')

    # 3.查询肉类的4个商品 和　3个新品
    meats = Goods.objects.get_goods_by_type(goods_type_id=MEAT, limit=4)
    meats_new = Goods.objects.get_goods_by_type(goods_type_id=3, limit=3, sort='new')

    # 4.查询蛋类的4个商品 和　3个新品
    eggs = Goods.objects.get_goods_by_type(goods_type_id=EGGS, limit=4)
    eggs_new = Goods.objects.get_goods_by_type(goods_type_id=4, limit=3, sort='new')

    # 5.查询蔬菜的4个商品 和　3个新品
    vegetables = Goods.objects.get_goods_by_type(goods_type_id=VEGETABLES, limit=4)
    vegetables_new = Goods.objects.get_goods_by_type(goods_type_id=5, limit=3, sort='new')

    # 6.查询水果的4个商品 和　3个新品
    frozens = Goods.objects.get_goods_by_type(goods_type_id=FROZEN, limit=4)
    frozens_new = Goods.objects.get_goods_by_type(goods_type_id=6, limit=3, sort='new')

    # 7.组织上下文数据
    context = {'fruits':fruits, 'fruits_new':fruits_new,
               'seafoods':seafoods, 'seafoods_new':seafoods_new,
               'meats':meats, 'meats_new':meats_new,
               'eggs':eggs, 'eggs_new':eggs_new,
               'vegetables':vegetables, 'vegetables_new':vegetables_new,
               'frozens':frozens, 'frozens_new':frozens_new
               }
    return render(request, 'df_goods/index.html', context)


# /goods/商品id
def goods_detail(request, gid):
    '''显示商品详情页面'''
    # 方法一　根据goods_id找商品　用goods的id属性调用Image管理器类中的方法获取图片
    # 1.根据商品id查询商品信息
    # goods = Goods.objects.get_goods_by_id(gid=gid)
    # 2.获取商品的详情图片
    # images = Image.objects.get_image_by_goods_id(gid=gid)
    # 方法二　在Goods的管理器类中定义一个方法　取出图片后goods.image = image
    # goods = Goods.objects.get_goods_by_id_with_image(goods_id=goods_id)
    # 方法三 方法二的基础上　把GoodsManager中获取图片的方法重新定义在一个Goods的新的管理器类中
    goods = Goods.objects_logic.get_goods_by_id(gid=gid)
    # 3,根据商品类型id 查询新品信息
    goods_new = Goods.objects.get_goods_by_type(goods_type_id=goods.goods_type_id, limit=2, sort='new')
    # todo:添加历史浏览记录
    # 如果用户未登录,不需要添加历史浏览记录
    if request.session.has_key('islogin'):
        passport_id = request.session.get('passport_id')
        BrowseHistory.objects.add_one_history(passport_id=passport_id, goods_id=gid)

    # 4.根据商品类型id在enums.py文件中查询商品类型名称
    type_title = GOODS_TYPE[goods.goods_type_id]
    # ５.使用模板文件
    context = {'goods':goods, 'goods_new':goods_new, 'type_title':type_title}
    return render(request, 'df_goods/detail.html', context)


# /list/商品类型id/页码/?sort=排序方式
def goods_list(request, goods_type_id, pindex):
    '''显示商品列表页面'''
    # 获取排序方式
    sort = request.GET.get('sort', 'default')
    # 根据goods_type_id查询商品信息
    goods_li = Goods.objects.get_goods_by_type(goods_type_id=goods_type_id, sort=sort)
    # 进行分页操作
    paginator = Paginator(goods_li, 5)
    # 获取第pindex页的内容
    pindex = int(pindex)
    goods_li = paginator.page(pindex)
    # 获取分页后的总页数
    nums_pages = paginator.num_pages
    # 控制页码列表
    if nums_pages < 5:
        # 如果不足5页　页码全显示
        pages = range(1, nums_pages+1)
    elif pindex <= 3:
        # 当前页是前三页,显示前５页
        pages = range(1, 6)
    elif nums_pages - pindex <= 2:
        # 当前页是最后3页,显示后5页
        pages = range(pindex-2, pindex+3)
    # 根据商品类型查询新品信息
    goods_new = Goods.objects.get_goods_by_type(         goods_type_id=goods_type_id, sort='new', limit=2)

    # 定义上下文
    context = {'goods_li': goods_li, 'type_id':goods_type_id, 'sort':sort,
               'type_title':GOODS_TYPE[int(goods_type_id)],
               'pages':pages, 'goods_new':goods_new}
    # 使用模板文件
    return render(request, 'df_goods/list.html', context)




























