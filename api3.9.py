import requests
import math

# url = "https://117.78.31.209:26335/rest/campusrtlswebsite/v1/clientlocation/heatmap"
# headers = {
#     "Content-Type": "application/json",
#     "X-Auth-Token": 'budDCq6r1SC/t5BlOdsANs86r84bRztFIGJ2QI9eEDk=',
#     "Accept": "application/json"
# }
# url = url + "?startTime=1624323600000&endTime=1624327200000"
# res = requests.post(url, headers=headers, verify=False)
# data = res.json()['data']

# # print(data)

import ssl
ssl._create_default_https_context = ssl._create_unverified_context
# 用户终端信息
import http.client
import json

conn = http.client.HTTPSConnection("117.78.31.209:26335")

headers = { 'x-auth-token': "budDCq6r1SC/t5BlOdsANs86r84bRztFIGJ2QI9eEDk=" }

conn.request("POST", "/rest/campusrtlswebsite/v1/clientlocation/lastlocation?param=%7B%22id%22%3A%22540d8574-a743-4cda-a47e-3718b6a4f722%22%2C%22level%22%3A3%2C%22type%22%3A%22floor%22%7D&=&=", headers=headers)

res = conn.getresponse()
data = res.read()

data = json.loads(data.decode("utf-8"))
# print(data["data"])
keys=['x', 'y']
datalist = []

for item in data["data"]:
    temp = {}
    for key in keys:
        # print(key,data["data"][item][key])
        temp[key]=data["data"][item][key]
    # print(temp)
    temp["value"]=1
    datalist.append(temp)

print(datalist)
# return json.dumps(datalist)