import hashlib
import os
import uuid

from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
# 首页
from django.urls import reverse

from AXF import settings
from app.models import Wheel, Nav, Shop, Mustbuy, MainShow, Foodtypes, Goods, User


def home(request):
    wheels = Wheel.objects.all()

    navs  =  Nav.objects.all()

    mustbuys = Mustbuy.objects.all()

    # 商品部分
    shoplist = Shop.objects.all()
    shophead = shoplist[0]
    shoptab = shoplist[1:3]
    shopclass = shoplist[3:7]
    shopcommend = shoplist[7:11]

    mainshows = MainShow.objects.all()


    data = {

        'wheels': wheels,

        'navs': navs,

        'mustbuys': mustbuys,

        'shophead': shophead,

        'shoptab': shoptab,

        'shopclass': shopclass,

        'shopcommend': shopcommend,

        'mainshows': mainshows
    }

    return render(request, 'home/home.html', context=data)


def market(request, categoryid, childid,sortid):

    # 分类数据
    foodtypes = Foodtypes.objects.all()

    typeIndex = int(request.COOKIES.get('typeIndex', 0))
    categoryid = foodtypes[typeIndex].typeid


    #子类

    childtypename = foodtypes.get(
        typeid=categoryid).childtypenames
    childlist =[]
    for item in childtypename.split('#'):
       arr = item.split(':')
       obj = {'childname':arr[0], 'childid':arr[1]}
       childlist.append(obj)



    if childid == '0':
        goodslist = Goods.objects.filter(categoryid=categoryid)


    else:
        goodslist = Goods.objects.filter(categoryid=categoryid, childcid=childid)


    # 商品数据

    if sortid == '1':  # 销量排序
        goodslist = goodslist.order_by('productnum')
    elif sortid == '2':  # 价格最低
        goodslist = goodslist.order_by('price')
    elif sortid == '3':  # 价格最高
        goodslist = goodslist.order_by('-price')

    data = {
        'foodtypes': foodtypes,
        'goodslist': goodslist,
        'childlist': childlist,
        'categoryid': categoryid,
        'childid': childid
    }


    return render(request, 'market/market.html', context=data)


def cart(request):
    return render(request, 'cart/cart.html')


# 我的
def mine(request):
    token = request.session.get('token')

    responseData = {
        'title': '我的',
        'name':'',
        'rank':'',
        'img':'',
        'islogin':False,
    }

    if token:   # 登录
        user = User.objects.get(token=token)
        responseData['name'] = user.name
        responseData['rank'] = user.rank
        responseData['img'] = '/static/uploads/' + user.img
        responseData['islogin'] = True


        # 获取订单信息
        # orders = Order.objects.filter(user=user)
        # payed = 0   # 已付款
        # wait_pay = 0    # 待付款
        # for order in orders:
        #     if order.status == 1:
        #         wait_pay += 1
        #     elif order.status == 2:
        #         payed += 1
        #
        # responseData['payed'] = payed
        # responseData['wait_pay'] = wait_pay

    else:       # 未登录
        responseData['name'] = '未登录'
        responseData['rank'] = '无等级(未登录)'
        responseData['img'] = '/static/uploads/atom.png'
        responseData['islogin'] = False


    return render(request, 'mine/mine.html', context=responseData)

def register(request):

    if request.method == 'POST':
        user = User()
        user.account = request.POST.get('account')
        user.password = generate_password(request.POST.get('password'))
        user.name = request.POST.get('name')
        user.tel = request.POST.get('tel')
        user.address = request.POST.get('address')

        imgName = user.account + '.png'
        imgPath = os.path.join(settings.MEDTA_ROOT, imgName )

        file = request.FILES.get('file')

        with open(imgPath, 'wb') as fp:
            for data in file.chunks():
                fp.write(data)
        user.img = imgName

        user.token = str(uuid.uuid5(uuid.uuid4(), 'register'))

        user.save()

        request.session['token'] = user.token


        return  redirect("axf:mine")

    elif request.method == 'GET':
        return render(request,'mine/register.html')


def generate_password(password):
    sha = hashlib.sha512()
    sha.update(password.encode('utf-8'))
    return sha.hexdigest()


def login(request):

    if request.method == 'POST':

        account = request.POST.get('account')
        password = request.POST.get('password')

        try:
            user = User.objects.get(account=account)

            if user.password != str(generate_password(password)):
                return render(request, 'mine/login.html', context={'error': '密码错误'})

            else:
                user.token = str(uuid.uuid5(uuid.uuid4(), 'login'))
                user.save()

                request.session['token'] = user.token
                return redirect('axf:mine')

        except:
            return render(request, 'mine/login.html', context={'error': '用户名错误'})

    elif request.method == 'GET':
        return render(request, 'mine/login.html')


def quit(request):

    # response = redirect(reverse('axf:mine'))
    # request.session.flush()
    logout(request)

    return redirect('axf:mine')


def checkuser(request):
    account = request.GET.get('account')
    try:
        user = User.objects.get(account = account)
        return JsonResponse({'status': '-1'})
    except:
        return JsonResponse({'status': '1'})
