from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from Train.forms import RegisterForm, LoginForm, TrainForm, ProblemForm
from django.contrib import messages

# Create your views here.
from .get_tickets import get_ticket
from .models import Users, Orders, Train, Problems
# type = {'商务座': 'sw_seat',
#         '一等座': 'one_seat',
#         '二等座': 'tow_seat',
#         '高级软卧': 'high_soft_lie',
#         '软卧': 'soft_lie',
#         '动卧': 'move_lie',
#         '硬卧': 'strong_lie',
#         '软座': 'soft_seat',
#         '硬座': 'strong_seat',
#         '无座': 'no_seat',
#         }
prices = {
        '商务座': '1998',
        '一等座': '969',
        '二等座': '576',
        '高级软卧': '500',
        '软卧': '455.5',
        '动卧': '300',
        '硬卧': '283.5',
        '软座': '235',
        '硬座': '156.5',
        '无座': '156.5',
}
def user_login(request):
    result = {}
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(request, username=username, password=password)
            user2 = Users.objects.filter(username=username)
            print(user, user2)
            if user:
                login(request, user)
                return redirect('/train/')
            else:
                if user2:
                    messages.error(request, '密码错误！')
                else:
                    messages.error(request, '用户不存在！')
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    # 退出登录
    logout(request)
    return redirect('/train/')


def user_register(request):
    if request.method == "POST":
        # 用提交的数据生成表单
        print("***************")
        form = RegisterForm(request.POST)
        # 能通过验证，返回True，否则返回False
        if form.is_valid():
            # 获取所有字段
            data = form.cleaned_data
            data.pop('password1')
            # 获取某个字段
            uname = form.cleaned_data.get('username', '')
            print(data)
            # 密码会做签名加密
            user1 = Users.objects.filter(username=uname)
            print(type(user1))
            if user1:
                messages.error(request, '用户名已存在，请重新注册！')
                return redirect('/register/')
            user = Users.objects.create_user(**data)
            if user:
                messages.error(request, '注册成功，请登录！')
                return redirect('/login/')
        else:
            return render(request, 'register.html', {'form': form})
    return render(request, 'register.html')


def change_password(request):
    if request.method == 'POST':
        # print("***************")
        password = request.POST.get('password', '')
        password1 = request.POST.get('password1', '')
        username = request.user.username
        print(password, password1)
        user = authenticate(request, username=username, password=password)
        if user:
            user.set_password(password1)
            user.save()
            messages.error(request, '密码修改成功，请重新登录！')
            return redirect('/login/')
    return render(request, 'change.html')


def search_train(request):
    if request.method == 'POST':
        form = TrainForm(request.POST)
        if form.is_valid():
            from_station_name = request.POST.get('from_station_name', '')
            to_station_name = request.POST.get('to_station_name', '')
            date = request.POST.get('date', '')
            trainList = Train.objects.filter(from_station_name=from_station_name, to_station_name=to_station_name, date=date)
            if trainList:
                return render(request, 'train.html', {'trains': trainList})
            else:
                get_ticket(date, from_station_name, to_station_name)
                trainList1 = Train.objects.filter(from_station_name=from_station_name, to_station_name=to_station_name, date=date)
                return render(request, 'train.html', {'trains': trainList1})
    return render(request, 'train.html')


def book_order(request):
    if request.method == "POST":
        # 用提交的数据生成表单
        id = request.POST.get('id')
        print(id)
        trainList = Train.objects.filter(id=id)
        return render(request, 'border.html', {'trains': trainList})
    return render(request, 'train.html')


def book_order1(request):
    if request.method == "POST":
        username = request.user.username
        oname = request.POST.get('oname')
        code = request.POST.get('code')
        ophone = request.POST.get('ophone')
        seat_type = request.POST.get('seat_type')
        train_code = request.POST.get('train_code')
        from_station_name = request.POST.get('from_station_name')
        to_station_name = request.POST.get('to_station_name')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        arrive_time = request.POST.get('arrive_time')
        print(seat_type, prices[seat_type])
        price = prices[seat_type]
        print(type(date))
        print(username, ophone, oname, code, seat_type, from_station_name, to_station_name, date, start_time, arrive_time,price)
        trainLinst = Train.objects.filter(train_code=train_code, date=date).first()
        print(trainLinst.train_code, trainLinst.date)
        res = Orders.objects.create(username=username, oname=oname, code=code, ophone=ophone,
                                    seat_type=seat_type, train_code=train_code, date=date,
                                    from_station_name=from_station_name, to_station_name=to_station_name,
                                    start_time=start_time, arrive_time=arrive_time, price=price)
        if res:
            if seat_type == '商务座':
                if trainLinst.sw_seat != '有':
                    ticket = int(trainLinst.sw_seat)
                    ticket = ticket - 1
                    trainLinst.sw_seat = ticket
                    trainLinst.save()
            if seat_type == '一等座':
                if trainLinst.one_seat != '有':
                    ticket = int(trainLinst.one_seat)
                    ticket = ticket - 1
                    trainLinst.one_seat = ticket
                    trainLinst.save()
            if seat_type == '二等座':
                if trainLinst.tow_seat != '有':
                    ticket = int(trainLinst.tow_seat)
                    ticket = ticket - 1
                    trainLinst.tow_seat = ticket
                    trainLinst.save()
            if seat_type == '高级软卧':
                if trainLinst.high_soft_lie != '有':
                    ticket = int(trainLinst.high_soft_lie)
                    ticket = ticket - 1
                    trainLinst.high_soft_lie = ticket
                    trainLinst.save()
            if seat_type == '软卧':
                if trainLinst.soft_lie != '有':
                    ticket = int(trainLinst.soft_lie)
                    # print(trainLinst.soft_lie)
                    ticket = ticket - 1
                    trainLinst.soft_lie = ticket
                    trainLinst.save()
            if seat_type == '动卧':
                if trainLinst.move_lie != '有':
                    ticket = int(trainLinst.move_lie)
                    ticket = ticket - 1
                    trainLinst.move_lie = ticket
                    trainLinst.save()
            if seat_type == '硬卧':
                if trainLinst.strong_lie != '有':
                    ticket = int(trainLinst.strong_lie)
                    ticket = ticket - 1
                    trainLinst.strong_lie = ticket
                    trainLinst.save()
            if seat_type == '软座':
                if trainLinst.soft_seat != '有':
                    ticket = int(trainLinst.soft_seat)
                    ticket = ticket - 1
                    trainLinst.soft_seat = ticket
                    trainLinst.save()
            if seat_type == '硬座':
                if trainLinst.strong_seat != '有':
                    ticket = int(trainLinst.strong_seat)
                    ticket = ticket - 1
                    trainLinst.strong_seat = ticket
                    trainLinst.save()
            if seat_type == '无座':
                if trainLinst.no_seat != '有':
                    ticket = int(trainLinst.no_seat)
                    ticket = ticket - 1
                    trainLinst.no_seat = ticket
                    trainLinst.save()

            orderList = Orders.objects.filter(username=username)
            messages.error(request, '预订成功！')
            return render(request, 'corder.html', {'orders': orderList})
        else:
            return render(request, 'train.html')
    return redirect('/train/')


def check_order(request):
    username = request.user.username
    orderList = Orders.objects.filter(username=username)
    return render(request, 'corder.html', {'orders': orderList})


def change_order(request):
    if request.method == "POST":
        # 用提交的数据生成表单
        id = request.POST.get('id')
        # print(id)
        orderList = Orders.objects.filter(id=id)
        return render(request, 'xorder.html', {'orders': orderList})
    return render(request, 'corder.html')

def search_train1(request):
    if request.method == 'POST':
        from_station_name = request.POST.get('from_station_name')
        to_station_name = request.POST.get('to_station_name')
        date = request.POST.get('date')
        print(from_station_name, to_station_name, date)
        trainList = Train.objects.filter(from_station_name=from_station_name, to_station_name=to_station_name, date=date)
        if trainList:
            return render(request, 'xorder.html', {'trains': trainList})
        else:
            get_ticket(date, from_station_name, to_station_name)
            trainList1 = Train.objects.filter(from_station_name=from_station_name, to_station_name=to_station_name, date=date)
            return render(request, 'xorder.html', {'trains': trainList1})
    return render(request, 'xorder.html')


def change_order1(request):
    if request.method == "POST":
        id = request.POST.get('id')
        trains = Train.objects.filter(id=id)
        return render(request, 'xcoder1.html', {'trains': trains})
    return render(request, 'corder.html')

def change_order2(request):
    if request.method == "POST":
        train_code = request.POST.get('train_code')
        from_station_name = request.POST.get('from_station_name')
        to_station_name = request.POST.get('to_station_name')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        arrive_time = request.POST.get('arrive_time')
        seat_type = request.POST.get('seat_type')
        price = prices[seat_type]
        print(seat_type, from_station_name, to_station_name, date, start_time, arrive_time, price)
        orders = Orders.objects.filter(from_station_name=from_station_name, to_station_name=to_station_name).first()
        print(orders.username, orders.train_code, orders.from_station_name, orders.to_station_name)
        trainLinst = Train.objects.filter(train_code=train_code, date=date).first()
        p1 = float(orders.price)
        p2 = float(price)
        print(p1, p2)
        if p1 > p2:
            c_price = p1-p2
            print(c_price)
            messages.error(request, '您的差价将稍后退回！')
        if orders:
            orders.train_code = train_code
            orders.date = date
            orders.seat_type = seat_type
            orders.start_time = start_time
            orders.arrive_time = arrive_time
            orders.price = price
            orders.save()

            if seat_type == '商务座':
                if trainLinst.sw_seat != '有':
                    ticket = int(trainLinst.sw_seat)
                    ticket = ticket - 1
                    trainLinst.sw_seat = ticket
                    trainLinst.save()
            if seat_type == '一等座':
                if trainLinst.one_seat != '有':
                    ticket = int(trainLinst.one_seat)
                    ticket = ticket - 1
                    trainLinst.one_seat = ticket
                    trainLinst.save()
            if seat_type == '二等座':
                if trainLinst.tow_seat != '有':
                    ticket = int(trainLinst.tow_seat)
                    ticket = ticket - 1
                    trainLinst.tow_seat = ticket
                    trainLinst.save()
            if seat_type == '高级软卧':
                if trainLinst.high_soft_lie != '有':
                    ticket = int(trainLinst.high_soft_lie)
                    ticket = ticket - 1
                    trainLinst.high_soft_lie = ticket
                    trainLinst.save()
            if seat_type == '软卧':
                if trainLinst.soft_lie != '有':
                    ticket = int(trainLinst.soft_lie)
                    ticket = ticket - 1
                    trainLinst.soft_lie = ticket
                    trainLinst.save()
            if seat_type == '动卧':
                if trainLinst.move_lie != '有':
                    ticket = int(trainLinst.move_lie)
                    ticket = ticket - 1
                    trainLinst.move_lie = ticket
                    trainLinst.save()
            if seat_type == '硬卧':
                if trainLinst.strong_lie != '有':
                    ticket = int(trainLinst.strong_lie)
                    ticket = ticket - 1
                    trainLinst.strong_lie = ticket
                    trainLinst.save()
            if seat_type == '软座':
                if trainLinst.soft_seat != '有':
                    ticket = int(trainLinst.soft_seat)
                    ticket = ticket - 1
                    trainLinst.soft_seat = ticket
                    trainLinst.save()
            if seat_type == '硬座':
                if trainLinst.strong_seat != '有':
                    ticket = int(trainLinst.strong_seat)
                    ticket = ticket - 1
                    trainLinst.strong_seat = ticket
                    trainLinst.save()
            if seat_type == '无座':
                if trainLinst.no_seat != '有':
                    ticket = int(trainLinst.no_seat)
                    ticket = ticket - 1
                    trainLinst.no_seat = ticket
                    trainLinst.save()

            messages.error(request, '改签成功！')
            return redirect('/corder/')
        else:
            messages.error(request, '改签失败！')
            return redirect('/corder/')
    return render(request, 'corder.html')

def cancel_order(request):
    if request.method == "POST":
        id = request.POST.get('id')
        order = Orders.objects.filter(id=id)
        res = order.delete()
        if res:
            messages.error(request, '退票成功！')
            return redirect('/corder/')
        else:
            messages.error(request, '退票失败！')
            return redirect('/corder/')
    return render(request, 'corder.html')


def problems(request):
    if request.method == "POST":
        username = request.user.username
        form = ProblemForm(request.POST)
        # 能通过验证，返回True，否则返回False
        if form.is_valid():
            problem = request.POST.get('problem')
            res = Problems.objects.create(username=username, problem=problem)
            if res:
                messages.error(request, '提交成功！')
                return redirect('/problem/')
            else:
                messages.error(request, '请重新提交！')
                return redirect('/problem/')
    return render(request, 'problem.html')






















# def forget_password(request):
#     form = ForgetForm()
#     if request.method == 'POST':
#         form = ForgetForm(request.POST)
#         if form.is_valid():
#             uphone = request.POST.get('uphone', '')
#             password1 = request.POST.get('password1', '')
#             user = Users.objects.filter(uphone=uphone).first()
#             print(user)
#             if user:
#                 print(user.password)
#                 user.password = password1
#                 user.save()
#                 return render(request, 'forget.html')
#     return render(request, 'forget.html', {'form': form})





