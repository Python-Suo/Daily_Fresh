from django.shortcuts import render,redirect
from df_user.models import Passport
from django.http import JsonResponse
from django.views.decorators.http import require_GET,require_POST,require_http_methods
from django.conf import settings
from django.core.mail import send_mail  # 导入发送邮件的函数
from df_user.tasks import send_register_success_mail # 导入任务函数
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
    return render(request, 'df_user/login.html', {'username':username})


#/user/login_check/
@require_POST
def login_check(request):
    '''用户登录校验'''
    # 1.接收用户名和密码
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember')
    # print(password)
    # 2.根据用户名和密码查找账户信息
    passport = Passport.objects.get_one_passport(username=username, password=password)
    # 3.判断结果并返回json数据
    if passport:
        # 用户名密码正确
        # print('hello')
        jres = JsonResponse({'res':1})
        if remember == 'true':
            jres.set_cookie('username',username)
        return jres
    else:
        # 用户名或密码错误
        return JsonResponse({'res':0})


def index(request):
    '''显示首页'''
    return render(request, 'df_user/index.html')





























