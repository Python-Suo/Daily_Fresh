from django.shortcuts import render,redirect
from df_user.models import Passport,Address
from django.http import JsonResponse
from django.views.decorators.http import require_GET,require_POST,require_http_methods
from django.conf import settings
from django.core.mail import send_mail  # 导入发送邮件的函数
from df_user.tasks import send_register_success_mail # 导入任务函数
from utils.decorators import login_required  # 导入登录判断装饰器函数
# Create your views here.


# /user/register/
# def register(request):
#     '''显示注册页面'''
#     return render(request, 'df_user/register.html')


# /user/register_handle/
# def register_handle(request):
#     '''用户信息注册'''
#     # 1.接收用户信息
#     username = request.POST['user_name']
#     password = request.POST['pwd']
#     email = request.POST['email']
#     # 2.将用户信息保存到数据库中
#     '''
#     passport = Passport()
#     passport.username = username
#     passport.password = password
#     passport.email = email
#     passport.save()
#     '''
#
#     '''
#     passport = Passport(username=username, password=password, email=email)
#     passport.save()
#     '''
#
#     Passport.objects.add_one_passport(username, password, email)
#     # 3.发送邮件给用户注册用的邮箱  这种方式是同步阻塞执行
#     # message = '<h1>恭喜您成为天天生鲜注册会员</h1>请保存好您的注册信息:<br>用户名:'+username+'<br>密码:'+password
#     # send_mail('注册成功信息','',settings.EMAIL_FROM, [email], html_message=message)
#
#     # 3.发送邮件给用户注册的邮箱　这种方式可以实现异步执行
#     send_register_success_mail.delay(username=username,password=password,email=email)
#     # 4.跳转到登录界面
#     return redirect('user/login')


# 将用户注册信息和对用户注册信息处理　放同一个函数
#/user/register
@require_http_methods(['GET', 'POST'])
def register(request):
    '''显示注册页面'''
    if request.method == 'GET':  # get是地址栏输入注册网址　访问注册网页
        return render(request, 'df_user/register.html')
    else:  # post方式　是页面表单填写信息的提交方式
        # 进行用户注册处理
        # 1.接收用户注册信息
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        # 2.将用户信息保存进数据库
        Passport.objects.add_one_passport(username, password, email)
        # 3.发送邮件给用户的注册邮箱
        send_register_success_mail.delay(username=username,password=password,email=email)
        # 4.跳转到登录页面
        return redirect('/user/login')


# /user/check_user_exist/
@require_GET
def check_user_exist(request):
    '''校验用户名是否存在'''
    # 1.获取用户名
    username = request.GET.get('username')
    # 2.根据用户名查询账户信息 get_one_passport(username)
    passport = Passport.objects.get_one_passport(username=username)
    # 3.如果查到,返回json{'res':0} 否则返回json{'res':1}
    if passport:
        # 用户名已存在
        return JsonResponse({'res':0})
    else:
        # 用户名可用
        return JsonResponse({'res':1})


#/user/login/
def login(request):
    '''显示登录页面'''
    # 1.判断是否有 username cookie
    if 'username' in request.COOKIES:   #　COOKIES是一个标准的字典
        # 获取用户名
        username = request.COOKIES['username']
    else:
        username = ''
    # 将cookie中的值传给模板变量username 用来执行记住用户名的操作
    return render(request, 'df_user/login.html', {'username':username})


# 使用模板文件时,除了代码中传递给模板文件的变量外,django会把request作为模板变量传给模板文件,request的相关
# 属性在模板文件中可以用　通过.运算符　模板变量的解析顺序


#/user/login_check/
@require_POST
def login_check(request):
    '''用户登录校验'''
    # 1.接收用户名和密码
    username = request.POST.get('username')
    password = request.POST.get('password')

    # 2.根据用户名和密码查找账户信息
    passport = Passport.objects.get_one_passport(username=username, password=password)
    # 3.判断结果并返回json数据
    if passport:
        # 用户名密码正确
        # 获取pre_url_path地址　未登录前访问的url地址
        if request.session.has_key('pre_url_path'):
            next = request.session['pre_url_path']
        else:
            next = '/'  # 默认跳转到首页
        jres = JsonResponse({'res': 1, 'next':next})
        # 判断是否要记住用户名
        remember = request.POST.get('remember')
        if remember == 'true':
            jres.set_cookie('username',username, max_age=14*24*3600)  # cookie没有默认时间
        # 记住用户的登录状态　服务器端用session
        request.session['islogin'] = True
        request.session['username'] = username
        # 记录登录账户的id
        request.session['passport_id'] = passport.id
        return jres
    else:
        # 用户名或密码错误
        return JsonResponse({'res':0})


# /user/logout
def logout(request):
    '''退出用户登录'''
    request.session.flush()  # 在数据库中的django_session表中删除此次会话的所有记录
                             # 清除用户的登录信息
    # request.session.clear() # 能去掉数据库中django_session表中session_data中的值部分
    # 跳转到首页
    return redirect('/user/')

#/user/

@login_required
def user(request):
    '''显示用户中心-个人信息页'''
    # 获取账户id
    passport_id = request.session['passport_id']
    # 1.获取登录用户的默认收货地址
    addr = Address.objects.get_one_address(passport_id=passport_id)
    return render(request, 'df_user/user_center_info.html', {'addr':addr,'page':'user'})


# /user/address
@login_required
@require_http_methods(['GET', 'POST'])
def address(request):
    '''显示用户中心-个人地址页'''
    # 获取账户id
    passport_id = request.session.get('passport_id')
    print(passport_id)
    print(passport_id)
    if request.method == 'GET':
        # 显示地址页面
        # 查询用户的默认地址
        addr = Address.objects.get_one_address(passport_id=passport_id)
        return render(request, 'df_user/user_center_site.html', {'addr':addr, 'page':'addr'})
    else:
        # 添加收货地址
        # 1.获取收货地址信息
        print('hello')
        recipient_name = request.POST.get('username')
        recipient_addr = request.POST.get('addr')
        recipient_phone = request.POST.get('phone')
        zip_code = request.POST.get('zip_code')
        # 2.添加进数据库
        Address.objects.add_one_address(passport_id=passport_id,
                                        recipient_name=recipient_name,
                                        recipient_addr=recipient_addr,
                                        recipient_phone=recipient_phone,
                                        zip_code=zip_code)
        # 3.刷新address页面　重定向
        return redirect('/user/address/')  # get方式访问




# /user/order
@login_required
def order(request):
    '''显示用户中心-个人订单页'''
    return render(request, 'df_user/user_center_order.html', {'page':'order'})































