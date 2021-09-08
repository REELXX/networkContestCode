import json
import requests
import math
import time
import numpy as np
from django.shortcuts import render, redirect
from django.http import JsonResponse
import random

requests.packages.urllib3.disable_warnings()
# if __name__ == "__main__":
# 获取token
url = "https://117.78.31.209:26335/rest/plat/smapp/v1/oauth/token"
headers = {
    "Content-Type": "application/json"
}
data = {
    "grantType": "password",
    "userName": "15659299492",
    "value": "zhenglinxin100"
}
response = requests.put(url, headers=headers, data=json.dumps(data), verify=False)
token = response.json()['accessSession']
print(token)

# 3.1智能评估体系
id_list = ['c94e9196-3686-4d4c-a7de-8117f581f63e', '9fc9253f-33a4-40db-8afc-825f383e54e8',
           '0504b1cb-e368-452c-8b43-2c8be81b3d14', '857b706e-67d9-49c0-b3cd-4bd1e6963c07']
test_inform = ['coverage', 'successCon', 'timeCon', 'throughput', 'capacity']
num = 0
eveg_are_inform = [[], [], [], []]
for i in id_list:
    url = ' https://117.78.31.209:26335/rest/campuswlanqualityservice/v1/expmonitor/overview/rate'
    param_0 = {"regionType": "site", "level": "0", "tenantId": "default-organization-id", "startTime": "1624053600000",
               "id": i, "endTime": "1624453200000"}
    header = {
        "X-Auth-Token": token,
        "Accept": "application/json;charset=UTF8",
        "Content-Type": "application/json",
    }
    res = requests.get(url, headers=header, params={'param': json.dumps(param_0)}, verify=False)
    #  print(res.json())
    res_inform = res.json()
    area_in = []
    for i in test_inform:
        area_in.append(res_inform['data']['values'][i])
    eveg_are_inform[num] = area_in
    num = num + 1


def rada(request):
    return JsonResponse({"inf1": [eveg_are_inform[0]], "inf2": [eveg_are_inform[1]], "inf3": [eveg_are_inform[2]],
                         "inf4": [eveg_are_inform[3]]})


# 3.2健康度趋势

trend_num = 0
trend_request_inform = ['coverage', 'rate', 'successCon', 'throughput', 'capacity']
rateall = [[], [], [], []]
coverageall = [[], [], [], []]
successConall = [[], [], [], []]
capacityall = [[], [], [], []]
throughputall = [[], [], [], []]
for i in id_list:
    url = ' https://117.78.31.209:26335/rest/campuswlanqualityservice/v1/expmonitor/rate/basictable?'
    param_0 = {"regionType": "site", "level": "0", "tenantId": "default-organization-id", "startTime": "1624053600000",
               "id": i, "endTime": "1624453200000"}
    header = {
        "X-Auth-Token": token,
        "Accept": "application/json;charset=UTF8",
        "Content-Type": "application/json",
    }
    res = requests.get(url, headers=header, params={'param': json.dumps(param_0)}, verify=False)

    res_inf = res.json()
    coverage_in = []
    rate_in = []
    successCon_in = []
    throughput_in = []
    capacity_in = []
    # print(res_inf['data'])
    # print(res_inf['data']['values'])
    # print(res_inf['data']['values'][2])

    for i in range(26):
        coverage_in.append(res_inf['data']['values'][i]['coverage'])
        rate_in.append(res_inf['data']['values'][i]['rate'])
        successCon_in.append(res_inf['data']['values'][i]['successCon'])
        throughput_in.append(res_inf['data']['values'][i]['throughput'])
        capacity_in.append(res_inf['data']['values'][i]['capacity'])

    rateall[trend_num] = rate_in
    coverageall[trend_num] = coverage_in
    successConall[trend_num] = successCon_in
    throughputall[trend_num] = throughput_in
    capacityall[trend_num] = capacity_in
    trend_num = trend_num + 1


def trendmap(request):
    return JsonResponse({"ratess": rateall, 'cover': coverageall, 'successcon': successConall, 'through': throughputall,
                         'capa': capacityall})


def monitor(request):
    return render(request, 'Home/monitor.html')


def other(request):
    return render(request, 'Home/other.html')


def monitorDetail(request):
    return render(request, 'Home/detail1.html')


def otherDetail(request):
    return render(request, 'Home/detail2.html')


def satisfaction(request):
    return render(request, 'Home/satisfaction.html')


import numpy as np
import matplotlib.pyplot as plt


# 求隶属度
def fcm_u(c, n, data, m):
    u = np.array([[float(0) for i in range(n)] for j in range(c)])
    for i in range(c):
        for j in range(n):
            sum = 0
            for k in range(c):
                temp = (np.linalg.norm(data[j, :] - c_new[i, :]) / np.linalg.norm(data[j, :] - c_new[k, :])) ** (
                        2.0 / (m - 1))
                sum += temp
            u[i][j] = float(1.0 / sum)
    u = np.array(u)
    return u


# 求聚类中心
def fcm_c(c, u, m, n, data, a):
    c_new = []
    u_ij_m = u ** 2
    c_c = (u_ij_m + 0.3 * a) @ data
    c_new = c_c / (np.sum(u_ij_m + 0.3 * a, 1, keepdims=True) @ np.ones((1, 6)))
    c = len(c_new)
    return c_new, c


def fcm(inter, n, m, data):  # inter:迭代次数 n:样本数  m:一般为2  data：数据集  c:类数
    global c_new
    data = np.array(data)
    # 初始化隶属度
    u = []
    c = 4
    # 速率，接入成功率，接入耗时，漫游达标率，信号与干扰，容量健康度
    c_new = [[32, 89.2, 21, 33, 45, 44],  # 正确
             [100, 89.2, 21, 33, 45, 44],  # rate速率
             [32, 89.2, 100, 33, 45, 44],  # 接入耗时timeCon
             [32, 89.2, 21, 0, 45, 44]]  # 漫游达标率
    c_new = np.array(c_new)
    for t in range(inter):
        # 求隶属度uij
        u = fcm_u(c, n, data, m)

        dis = np.array([[float(0) for q in range(n)] for j in range(c)])
        for i1 in range(c):
            for j in range(n):
                dis[i1, j] = np.linalg.norm(data[j, :] - c_new[i1, :])
        sort_dis = np.sort(dis)
        min_sort_dis = sort_dis[1, :]
        min_sort_dis_2 = min_sort_dis
        sum_sort_2 = np.sum(dis, 0)
        a_jj = min_sort_dis_2 / sum_sort_2
        exp_a_jj = np.ones((c, 1))
        a_j = a_jj * exp_a_jj
        # 求聚类中心Ci
        c_new, c = fcm_c(c, u, m, n, data, a_j)
    return u, c_new


def loadDataSet(fileName):  # 得到数据集的数据
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArray = line.strip().split(' ')
        dataMat.append(
            [float(lineArray[0]), float(lineArray[1]), float(lineArray[2]), float(lineArray[3]), float(lineArray[4]),
             float(lineArray[5])])  # 添加数据
    return dataMat


queList = []

# 主函数

# 生成高斯分布的随机点
means1 = [32, 89.2, 21, 33, 45, 44]
cov1 = np.eye(6) * 2
means2 = [100, 89.2, 21, 33, 45, 44]
cov2 = np.eye(6) * 2
means3 = [32, 89.2, 100, 33, 45, 44]
cov3 = np.eye(6) * 2
means4 = [32, 89.2, 21, 0, 45, 44]
cov4 = np.eye(6) * 2
data1 = np.random.multivariate_normal(means1, cov1, 100)
data2 = np.random.multivariate_normal(means2, cov2, 100)
data3 = np.random.multivariate_normal(means3, cov3, 100)
data4 = np.random.multivariate_normal(means4, cov4, 100)
data = np.vstack((data1, data2, data3, data4))
U, C = fcm(20, len(data), 2, data)
dataMat = [[32.24277586, 88.00280528, 20.57829836, 31.74397164, 43.75964395, 42.43778038],
           [29.98704003, 90.34754347, 21.97877372, 33.31555032, 44.25127479, 44.87037341],
           [31.47028282, 88.87690192, 18.74858385, 33.19088776, 44.96072857, 44.86733174],
           [32.154147, 88.0174189, 20.75032569, 32.8308963, 47.80965206, 43.46530213],
           [32.98047896, 90.28955095, 20.48190384, 31.00377041, 43.74474885, 46.34298369],
           [100.22427249, 89.66891903, 19.49586265, 33.30366252, 44.84399543, 44.38620439],
           [98.91386345, 86.88619333, 21.15653264, 34.85350047, 45.20070367, 44.34336512],
           [98.6438615, 89.09825824, 21.15803034, 34.44882292, 44.85170896, 44.19793814],
           [100.76248192, 87.88341751, 20.6107849, 34.35669861, 46.28748639, 42.00307811],
           [101.59526755, 91.9637862, 20.3444201, 34.36086199, 46.3218226, 45.24131951],
           [101.41787933, 86.01723063, 22.12335837, 34.65944799, 44.40702234, 43.25655351],
           [32.84594444, 88.37563786, 100.96859151, 31.72708431, 45.1863847, 44.01721562],
           [30.02053272, 92.29890679, 101.2051303, 32.66914331, 44.86670786, 43.41566105],
           [29.96851861, 89.92184147, 98.060783, 34.05759969, 43.41425224, 41.85408797],
           [34.59479743, 89.06386419, 100.51903813, 35.1457628, 46.39851924, 43.86783592],
           [32.80846435, 90.41754888, 99.17201153, 30.49668114, 43.56561671, 43.9894182],
           [30.23523581, 90.20371509, 20.16209673, 9.23829465, 40.62672765, 40.55022952],
           [30.20087147, 80.98712676, 10.98851073, 2.47711841, 40.47414021, 40.52840054],
           [30.29394596, 90.19071149, 10.7752872, 1.29141783, 40.39666337, 40.3776614],
           [30.51073738, 80.84345879, 20.27158386, 7.08289937, 40.69193309, 40.51524089],
           [30.15953653, 90.00119612, 20.27342338, 1.89773744, 40.29511474, 40.3046079]]
dataMat = np.array(dataMat)
shuju1, shuju2, shuju3, shuju4 = [], [], [], []
Data = [[float(0) for q in range(len(C))] for p in range(len(dataMat))]
for i in range(len(dataMat)):
    for j in range(len(C)):
        dis = ((dataMat[i][0] - C[j][0]) ** 2 + (dataMat[i][1] - C[j][1]) ** 2 + (dataMat[i][1] - C[j][1]) ** 2 + (
                dataMat[i][2] - C[j][2]) ** 2 + (dataMat[i][3] - C[j][3]) ** 2 + (
                       dataMat[i][4] - C[j][4]) ** 2 + (dataMat[i][5] - C[j][5]) ** 2) ** 0.5
        Data[i][j] = dis
Data = np.array(Data)
for i in range(len(Data)):
    if Data[i][0] < Data[i][1] and Data[i][0] < Data[i][2] and Data[i][0] < Data[i][3]:
        shuju1.append(list(dataMat[i]))
    elif Data[i][1] < Data[i][0] and Data[i][1] < Data[i][2] and Data[i][1] < Data[i][3]:
        shuju2.append(list(dataMat[i]))
    elif Data[i][2] < Data[i][0] and Data[i][2] < Data[i][1] and Data[i][2] < Data[i][3]:
        shuju3.append(list(dataMat[i]))
    elif Data[i][3] < Data[i][0] and Data[i][3] < Data[i][2] and Data[i][3] < Data[i][1]:
        shuju4.append(list(dataMat[i]))
print(shuju4)
# shuju1 正常
# shuju2 速率问题 问题1
# shuju3 接入耗时问题 问题2
# shuju4 漫游达标率问题 问题3


for i in range(4):
    rdata = random.randrange(1, 30)
    hdata = random.randrange(12, 24)
    mdata = random.randrange(30, 60)
    sdata = random.randrange(1, 60)
    # 问题1的字典
    que1Dict = {'problemType': 'AP上传速率出现异常',
                'deviceRole': 'AR3200',
                'problem': shuju2[i][0],
                'lastTime': f'2021/8/{rdata} {hdata}:{mdata}:{sdata}',
                }
    # 问题2的字典

    que2Dict = {'problemType': '接入耗时过久',
                'deviceRole': 'AR120',
                'problem': shuju3[i][2],
                'lastTime': f'2021/8/{rdata} {hdata}:{mdata}:{sdata}',
                }
    # 问题3的字典

    que3Dict = {'problemType': '漫游达标率过低',
                'deviceRole': 'AR160',
                'problem': shuju4[i][3],
                'lastTime': f'2021/8/{rdata} {hdata}:{mdata}:{sdata}',
                }
    num = random.randrange(1, 4)
    if num is 1:
        queList.append(que1Dict)
        queList.append(que2Dict)
    elif num is 2:
        queList.append(que2Dict)
        queList.append(que3Dict)
    else:
        queList.append(que1Dict)
        queList.append(que3Dict)


def errorDetectInfo(request):
    print(queList)
    return JsonResponse({'question': queList})

def errorDetect1(request):
    return render(request, 'Home/errorDetect1.html')
# satisF = main()
#
#
# def manyidu(request):
#     return JsonResponse({'STSF': satisF})

# 热力图

# 获取token
# 拿到热力图


def getheatmap():
    url = "https://117.78.31.209:26335/rest/campusrtlswebsite/v1/clientlocation/heatmap"
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": token,
        "Accept": "application/json"
    }
    url = url + "?startTime=1624323600000&endTime=1624327200000"
    res = requests.post(url, headers=headers, verify=False)
    data = res.json()['data']

    # 处理data
    min_data = 10000
    max_data = 0
    for d in data:
        if min_data > d['count']:
            min_data = d['count']

        if max_data < d['count']:
            max_data = d['count']

    error = max_data - min_data
    res_data = []
    for d in data:
        d['value'] = math.floor(d['count'] / error * 50)
        d.pop('count')
    print("热力图数据加载完成")
    return data


def heart_map(request):
    heatmap_data = getheatmap()
    return JsonResponse({'sss': heatmap_data})


# 用户终端信息

def getUserDeviveMap():
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    # 用户终端信息
    import http.client
    import json
    conn = http.client.HTTPSConnection("117.78.31.209:26335")
    headers = {'x-auth-token': "budDCq6r1SC/t5BlOdsANs86r84bRztFIGJ2QI9eEDk="}
    conn.request("POST",
                 "/rest/campusrtlswebsite/v1/clientlocation/lastlocation?param=%7B%22id%22%3A%22540d8574-a743-4cda-a47e-3718b6a4f722%22%2C%22level%22%3A3%2C%22type%22%3A%22floor%22%7D&=&=",
                 headers=headers)

    res = conn.getresponse()
    data = res.read()

    data = json.loads(data.decode("utf-8"))
    # print(data["data"])
    keys = ['x', 'y']
    datalist = []

    for item in data["data"]:
        temp = {}
        for key in keys:
            # print(key,data["data"][item][key])
            temp[key] = data["data"][item][key]
        # print(temp)
        temp["value"] = 100
        datalist.append(temp)

    # print(datalist)
    return datalist


def heart_map2(request):
    userheatmap_data = getUserDeviveMap()
    return JsonResponse({'userXY': userheatmap_data})
