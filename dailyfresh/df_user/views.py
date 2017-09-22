from django.shortcuts import render,redirect
from df_user.models import Passport
# Create your views here.

# /user/register/
def register(request):
    '''显示注册页面'''
    return render(request, 'df_user/register.html')


def register_handle(request):
    '''用户信息注册'''
    # 1.接收用户信息
    username = request.POST['user_name']
    password = request.POST['pwd']
    email = request.POST['email']
    # 2.将用户信息保存到数据库中
    '''
    passport = Passport()
    passport.username = username
    passport.password = password
    passport.email = email
    passport.save()
    '''

    '''
    passport = Passport(username=username, password=password, email=email)
    passport.save()
    '''

    Passport.objects.add_one_passport(username, password, email)

    # 3.跳转到登录界面
    return redirect('user/login')