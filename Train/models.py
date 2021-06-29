from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class Train(models.Model):
    train_code = models.CharField(" 车次 ", max_length=20)
    from_station_name = models.CharField("出发车站", max_length=20)
    to_station_name = models.CharField("到达车站", max_length=20)
    date = models.CharField("日期", max_length=20)
    start_time = models.TimeField("出发时间", max_length=20)
    arrive_time = models.TimeField("到达时间", max_length=20)
    sw_seat = models.CharField("商务座", max_length=20)
    one_seat = models.CharField(" 一等座", max_length=20)
    tow_seat = models.CharField("二等座", max_length=20)
    high_soft_lie = models.CharField("高级软卧", max_length=20)
    soft_lie = models.CharField("软卧", max_length=20)
    move_lie = models.CharField("动卧", max_length=20)
    strong_lie = models.CharField("硬卧", max_length=20)
    soft_seat = models.CharField("软座", max_length=20)
    strong_seat = models.CharField("硬座", max_length=20)
    no_seat = models.CharField("无座", max_length=20)
    remark = models.CharField("备注", max_length=20)

    class Meta:
        db_table = 'trains'
        verbose_name = '火车票'
        verbose_name_plural = verbose_name

class Users(AbstractUser):
    username = models.CharField("用户名", unique=True, max_length=20)
    # code = models.CharField("身份证号", max_length=20)
    uphone = models.CharField("手机号", unique=True, max_length=20)
    password = models.CharField("密码", max_length=100)

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

class Orders(models.Model):
    # ForeignKey第一个参数：参照的模型类
    # on_delete CASCADE级联删除
    username = models.CharField("用户名", max_length=20)
    oname = models.CharField("真实姓名", max_length=20)
    code = models.CharField("身份证号", max_length=20)
    ophone = models.CharField("联系电话", max_length=20)
    start_time = models.TimeField("出发时间", max_length=20)
    arrive_time = models.TimeField("到达时间", max_length=20)
    train_code = models.CharField(" 车次 ", max_length=20)
    from_station_name = models.CharField("出发车站", max_length=20)
    to_station_name = models.CharField("到达车站", max_length=20)
    seat_type = models.CharField("座位类型", max_length=20)
    date = models.CharField("日期", max_length=20)
    price = models.CharField("价格", max_length=20)

    class Meta:
        db_table = 'orders'
        verbose_name = '车票订单'
        verbose_name_plural = verbose_name


class Problems(models.Model):
    username = models.CharField("用户名", max_length=20)
    problem = models.CharField("意见反馈", max_length=200)

    class Meta:
        db_table = 'problems'
        verbose_name = '用户意见反馈'
        verbose_name_plural = verbose_name
