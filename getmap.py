import requests

import json
import requests
from pandas.io.json import json_normalize
from pyecharts.charts import Map
from pyecharts import options as opts

#获取用户ip
def get_ip_info(ip):
    r = requests.get("http://ip.taobao.com/outGetIpInfo?ip=%s&accessKey=alibaba-inc" %ip)
    if r.json()['code']==0:
        data = r.json()['data']
        country = data['country']
        region = data['region']
        city = data['city']
        area = data['area']
        isp = data['isp']

        print("IP地址:%s\n所属：%s%s%s%s\n运营商：%s\n" %(ip,country,region,city,area,isp))
        return country,region,city,area,isp
    else:
        print('查询错误')
        return False


####################
####生成疫情地图####
####################

def get_covid19_map(Country = '中国',region = '天津'):

    """功能：请求疫情数据,来自网易"""

    url="https://c.m.163.com/ug/api/wuhan/app/data/list-total"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}
    ret=requests.get(url, headers=headers)
    result=json.loads(ret.content)

    #####处理数据######
    datalist = result['data']['areaTree']
    #定位到国家
    for item in datalist:
        if item['name']== Country:
            CountryData = item
    #定位到区域
    for item in CountryData['children']:
        if item['name']== region:
            regionData = item
    #格式化数据
    temp = regionData['children']
    js2pd = json_normalize(temp)

    #####绘图######
    name = list(js2pd['name'])
    totalConfirm = list(js2pd['total.confirm'])
    totdayConfirm = sum(list(js2pd['today.confirm']))
    js2pd['today.confirm'].fillna(0,inplace=True)
    todayConfirm=int(sum(js2pd['today.confirm']))
    date = js2pd['lastUpdateTime'][0]

    mapDataList = [[name[i], totalConfirm [i]] for i in range(len(name))]
    
    map = Map()
    map.set_global_opts(
        title_opts=opts.TitleOpts(title="新型冠状病毒疫情累积确诊分布地图""\n今日确诊："+str(todayConfirm),
        pos_left='center',  # 标题位置
        subtitle='更新日期:'+str(date), # 副标题
        ),
        visualmap_opts=opts.VisualMapOpts(max_=50, is_piecewise=True,
                                        pieces=[
                                            {"max": 999999, "min": 10000, "label": ">100000", "color": "#a10000"},
                                            {"max": 9999, "min": 1000, "label": "9999-1000", "color": "#fa0000"},
                                            {"max": 999, "min": 500, "label": "500-999", "color": "#ff6666"},
                                            {"max": 499, "min": 100, "label": "100-499", "color": "#ff8787"},
                                            {"max": 99, "min": 10, "label": "10-99", "color": "#ffbdbd"},
                                            {"max": 9, "min": 1, "label": "1-9", "color": "#ffebeb"},
                                            {"max": 0, "min": 0, "label": "0", "color": "#ffffff"},
                                        ])
        )
    map.add("" ,mapDataList, maptype=region)
    map.render("21-8-17-1643/covid19Map/map.html")


#main
ip = "211.94.236.169"
_,region,_,_,_ = get_ip_info(ip)
get_covid19_map()
