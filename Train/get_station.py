import requests, re
url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8971"
response = requests.get(url)
# 将车站的名字和编码进行提取
station = re.findall(r'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
station_code = dict(station)
#进行交换
station_names = dict(zip(station_code.values(), station_code.keys()))
#打印出得到的车站字典
# print(station_names)

#print(station_code)
