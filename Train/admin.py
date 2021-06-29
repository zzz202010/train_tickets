from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from .models import Users, Train, Orders, Problems

admin.site.register(Users, UserAdmin)

@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    # 列表页属性
    list_display = ['train_code', 'from_station_name', 'to_station_name', 'date', 'start_time', 'arrive_time',  'sw_seat', 'one_seat', 'tow_seat', 'high_soft_lie', 'soft_lie', 'move_lie', 'strong_lie', 'soft_seat', 'strong_seat', 'no_seat',  'remark']
    #list_filter = ['train_code']
    search_fields = ['train_code']

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['username', 'oname', 'code', 'ophone', 'train_code', 'from_station_name', 'to_station_name', 'date', 'start_time', 'arrive_time', 'price']
    #list_filter = ['username']
    search_fields = ['username']

@admin.register(Problems)
class ProblemsAdmin(admin.ModelAdmin):
    list_display = ['username', 'problem']
    #list_filter = ['username']
    search_fields = ['username']

admin.site.site_header = '火车票购票系统后台'
admin.site.site_title = '火车票购票系统'
