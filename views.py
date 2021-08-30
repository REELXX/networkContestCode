import http.client
import ssl
import json
import time

ssl._create_default_https_context = ssl._create_unverified_context

conn = http.client.HTTPSConnection("117.78.31.209:26335")

payload = "{\"endTime\":1628507381000,\"startTime\":1628438400000,\"userMac\":\"c4-9e-d3-d2-d9-da\"}"

headers = {
    'x-auth-token': "budDCq6r1SC/t5BlOdsANs86r84bRztFIGJ2QI9eEDk=",
    'content-type': "application/json"
}

conn.request("POST", "/rest/campusclientwebsite/v1/journey/nodelist?=&=", payload, headers)

res = conn.getresponse()
data = res.read().decode("utf-8")
data = json.loads(data)

a = 0
for i in data['data']:
    try:
        # 时间戳处理
        if float(i['accTime']) > 162847546100:
            i['accTime'] = float(i['accTime']) / 1000
        timestamp = float(i['accTime'])

        timeArray = time.localtime(timestamp)

        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

        i['accTime'] = otherStyleTime

    except Exception as e:
        print("shibai")
# L1 = []
# for i in range(len(data['data'])):
#     try:
#         L1.append(data['data'][i]['nodeKpi']['duration'])
#         print(data['data'][i]['accTime'])
#         print(L1)
#     except:
#         L1.append('异常')
# for i in range(30):
#     try:
#         if int(data["data"][i]['nodeKpi']['duration']) < 1:
#             data["data"][i]['nodeKpi']['duration'] = 0
#         print(data["data"][i]['nodeKpi']['duration'])
#     except:
#         print("用户信息错误")
import random

accTime = []
liveTime = []
jourDir = {}
jourList = []
situation = []
color = []
for i in range(len(data['data'])):
    pingFen = random.randrange(80, 100)
    accTime.append(data['data'][i]['accTime'])

    try:
        liveTime.append(data['data'][i]['nodeKpi']['duration'])
        # print(data['data'][i]['accTime'])
        # print(liveTime)
    except:
        liveTime.append(0)
    if liveTime[i] == 0 :
        situation.append("接入错误")
        color.append('#FF000')
    else:
        situation.append("接入成功")
        color.append('#5dd375')
    jourDir = {'accTime': data['data'][i]['accTime'], 'huoyuetime': liveTime[i],
               'pingfen': pingFen,'color':color[i],}

    jourList.append(jourDir)
print(situation)