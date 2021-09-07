# import requests
# import json
#
# url = "https://117.78.31.209:26335/rest/plat/smapp/v1/oauth/token"
# headers = {
#     "Content-Type": "application/json"
# }
# data = {
#     "grantType": "password",
#     "userName": "15659299492",
#     "value": "zhenglinxin100"
# }
# response = requests.put(url, headers=headers, data=json.dumps(data), verify=False)
# token = response.json()['accessSession']
#
# url = "https://117.78.31.209:26335/rest/campusclientservice/v1/event/userlist"
# data = {
#     "regionType": "site", "level": "1", "tenantId": "default-organization-id", "startTime": "1624202262000",
#     "id": "857b706e-67d9-49c0-b3cd-4bd1e6963c07",
#     "endTime": "1624461462433",
#     "sortColumn": "totalcount",
#     "currPage": "1",
#     "pageSize": "100",
#     "sortType": "desc"
# }
# header = {
#     "X-Auth-Token": token,
#     "Accept": "application/json;charset=UTF8",
#     "Content-Type": "application/json",
# }
# res = requests.post(url, headers=header, data=json.dumps(data), verify=False)
# # print(res.json())
# people_dir = res.json()
#
# latency = []
# linkQuality = []
# for i in range(len(people_dir['data']['tableData'])):
#     latency.append(people_dir['data']['tableData'][i]['latency'])
#     linkQuality.append(people_dir['data']['tableData'][i]['linkQuality'])
#
#
# print(latency)
# print(linkQuality)
import random

for i in range(10):
    num = random.randrange(1, 4)
    print(num)