import random

import requests
import json
from prettytable import PrettyTable

from .get_station import station_code, station_names
from .models import Train
'''
train_date就是你查询的日期
from_station是武汉火车站的车站代号
to_station是到达火车站的车站代号
purpose_codes是成人还是学生
'''

def get_ticket(date, from_station ,to_station):
    date = date
    from_station = station_code[from_station]
    to_station = station_code[to_station]
    train_url = "https://kyfw.12306.cn/otn/leftTicket/query?"
    train_urls = train_url + "leftTicketDTO.train_date=" + date + "&leftTicketDTO.from_station=" + from_station + "&leftTicketDTO.to_station=" + to_station + "&purpose_codes=ADULT"
    cookie = '''Cookie: _uab_collina=161620823497726375024838; JSESSIONID=5C2B40AAA196F3E439471592A669A697; RAIL_EXPIRATION=1616487178247; RAIL_DEVICEID=pkoON4Ml4bFB8qAoGtUeGvk7-KhTKc4BKoVMmCw1YpGf4sB6Ybj-OOD2dqEGGaP1tjn4F8j3EL5yI9Q7fAgbNOkJwJt34zg9iiYbOfsytEzEB4ljG-AM8GmkSdrR4IKVILDjS7pMLGA07t5GgvD5xOo2nseIpjU1; route=6f50b51faa11b987e576cdb301e545c4; BIGipServerotn=451936778.24610.0000; _jc_save_fromStation=CQW%2CSHH; _jc_save_toStation=LYF%2CBJP; _jc_save_fromDate=2021-03-25; _jc_save_toDate=2021-03-25; _jc_save_wfdc_flag=wf'''
    header_list = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) ',
                   'Chrome/65.0.3325.181 Safari/537.36',
                   'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Maxthon2.0',
                   'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
                   'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
                   'Mozilla/5.0(Android;Linuxarmv7l;rv:5.0)Gecko/Firefox/5.0fennec/5.0')
    ticket = requests.get(train_urls, headers={'User-Agent': random.choice(header_list), 'Cookie': cookie})
    ticket.raise_for_status()  # 如果发送了一个错误的请求，会抛出异常
    ticket.content.decode("utf-8")
    ticket = json.loads(ticket.text)
    # print(ticket)
    # table = PrettyTable(
    #     [" 车次 ", "车编号", "出发车站", "到达车站", "出发时间", "到达时间", " 历时 ", "车开始站编号", "车结束站编号", "商务座", " 一等座", "二等座", "高级软卧", "软卧", "动卧", "硬卧", "软座", "硬座",
    #      "无座", "其他", "类型", "备注"])
    for i in ticket['data']['result']:
        data = {
            'train_code': '',
            # 'train_no': '',
            'from_station_name': '',
            'to_station_name': '',
            'date': '',
            'start_time': '',
            'arrive_time': '',
            # 'go_time': '',
            # 'from_station_no': '',
            # 'to_station_no': '',
            'sw_seat': '',
            'one_seat': '',
            'tow_seat': '',
            'high_soft_lie': '',
            'soft_lie': '',
            'move_lie': '',
            'strong_lie': '',
            'soft_seat': '',
            'strong_seat': '',
            'no_seat': '',
            # 'other': '',
            # 'seat_types': '',
            'remark': ''
        }
        item = i.split('|')  # 使用“|”进行分割
        # print(item)
        # data['train_no'] = item[2]
        data['train_code'] = item[3]  # 获取车次信息，在3号位置
        data['from_station_name'] = station_names[item[6]]  # 始发站信息在6号位置
        data['to_station_name'] = station_names[item[7]]  # 终点站信息在7号位置
        data['date'] = date
        data['start_time'] = item[8]  # 出发时间在8号位置
        data['arrive_time'] = item[9]  # 抵达时间在9号位置
        # data['go_time'] = item[10]  # 经历时间在10号位置
        # data['from_station_no'] = item[16]
        # data['to_station_no'] = item[17]
        data['sw_seat'] = item[32] or item[25]  # 特别注意，商务座在32或25位置
        data['one_seat'] = item[31]  # 一等座信息在31号位置
        data['tow_seat'] = item[30]  # 二等座信息在30号位置
        data['high_soft_lie'] = item[21]  # 高级软卧信息在21号位置
        data['soft_lie'] = item[23]  # 软卧信息在23号位置
        data['move_lie'] = item[27]  # 动卧信息在27号位置
        data['strong_lie'] = item[28]  # 硬卧信息在28号位置
        data['soft_seat'] = item[24]  # 软座信息在24号位置
        data['strong_seat'] = item[29]  # 硬座信息在29号位置
        data['no_seat'] = item[26]  # 无座信息在26号位置
        # data['other'] = item[22]  # 其他信息在22号位置
        # data['seat_types'] = item[35]
        data['remark'] = item[1]  # 备注信息在1号位置
        print(data)
        Train.objects.create(**data)
        # train_no = item[2]
        # from_station_no = item[16]
        # to_station_no = item[17]
        # seat_types = item[35]
        # price_url = "https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?"
        # price_urls = price_url + "train_no=" + train_no + "&from_station_no=" + from_station_no + "&to_station_no=" + to_station_no + "&seat_types=" + seat_types + "&train_date=" + date
        # print(price_urls)
        # try:
        #     prices = requests.get(price_urls, headers = {'User-Agent':random.choice(header_list),'Cookie':cookie})
        #     prices.raise_for_status()  # 如果发送了一个错误的请求，会抛出异常
        #     prices.content.decode("utf-8")
        # except:
        #     print("get price request Failed")
        #     return
        # try:
        #     print(type(prices.text))
        #     r_price = json.loads(prices.text)
        # except json.decoder.JSONDecodeError:
        #     print("错误")
        #     return
        # # print(r_price)
        # if 'data' in r_price:
        #     price = r_price['data']
        # else:
        #     print("r_price data invalid")
        #     return None
        # price = dict(price)
        # print(price)

