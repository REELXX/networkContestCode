import numpy as np
import matplotlib.pyplot as plt
import random
queList= []
#求隶属度
def fcm_u(c,n,data,m):
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
#求聚类中心
def fcm_c(c,u,m,n,data,a):
    c_new = []
    u_ij_m = u**2
    c_c = (u_ij_m + 0.3*a)@data
    c_new = c_c/(np.sum(u_ij_m+0.3*a,1,keepdims = True)@np.ones((1,6)))
    c = len(c_new)
    return c_new,c
def fcm(inter,n,m,data):  #inter:迭代次数 n:样本数  m:一般为2  data：数据集  c:类数
    global c_new
    data = np.array(data)
    #初始化隶属度
    u = []
    c = 4
    #速率，接入成功率，接入耗时，漫游达标率，信号与干扰，容量健康度
    c_new = [[32,89.2,21,33,45,44], #正确
             [100,89.2,21,33,45,44],#rate速率
             [32,89.2,100,33,45,44],#接入耗时timeCon
             [32,89.2,21,0,45,44]]#漫游达标率
    c_new = np.array(c_new)
    for t in range(inter):
        # 求隶属度uij
        u = fcm_u(c, n, data, m)

        dis = np.array([[float(0) for q in range(n)] for j in range(c)])
        for i1 in range(c):
            for j in range(n):
                dis[i1, j] = np.linalg.norm(data[j, :] - c_new[i1, :])
        sort_dis = np.sort(dis)
        min_sort_dis = sort_dis[1,:]
        min_sort_dis_2 = min_sort_dis
        sum_sort_2 = np.sum(dis,0)
        a_jj = min_sort_dis_2/sum_sort_2
        exp_a_jj = np.ones((c,1))
        a_j = a_jj*exp_a_jj
        # 求聚类中心Ci
        c_new, c = fcm_c(c, u, m, n, data, a_j)
    return u,c_new

def loadDataSet(fileName):      #得到数据集的数据
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArray = line.strip().split(' ')
        dataMat.append([float(lineArray[0]), float(lineArray[1]), float(lineArray[2]), float(lineArray[3]), float(lineArray[4]), float(lineArray[5])])  # 添加数据
    return  dataMat
#主函数
# def main():
#     #生成高斯分布的随机点
#     means1 = [32,89.2,21,33,45,44]
#     cov1 = np.eye(6) * 2
#     means2 = [100,89.2,21,33,45,44]
#     cov2 = np.eye(6) * 2
#     means3 = [32,89.2,100,33,45,44]
#     cov3 = np.eye(6) * 2
#     means4 = [32,89.2,21,0,45,44]
#     cov4 = np.eye(6) * 2
#     data1 = np.random.multivariate_normal(means1, cov1, 100)
#     data2 = np.random.multivariate_normal(means2, cov2, 100)
#     data3 = np.random.multivariate_normal(means3, cov3, 100)
#     data4 = np.random.multivariate_normal(means4, cov4, 100)
#     data = np.vstack((data1,data2,data3,data4))
#     U,C = fcm(20,len(data),2,data)
#     dataMat = loadDataSet('text.txt')   #提取数据集
#     dataMat = np.array(dataMat)
#     shuju1,shuju2,shuju3,shuju4 = [],[],[],[]
#     Data = [[float(0) for q in range(len(C))] for p in range(len(dataMat))]
#     for i in range(len(dataMat)):
#         for j in range(len(C)):
#             dis = ((dataMat[i][0]-C[j][0])**2+(dataMat[i][1]-C[j][1])**2+(dataMat[i][1]-C[j][1])**2+(dataMat[i][2]-C[j][2])**2+(dataMat[i][3]-C[j][3])**2+(dataMat[i][4]-C[j][4])**2+(dataMat[i][5]-C[j][5])**2)**0.5
#             Data[i][j] = dis
#     Data = np.array(Data)
#     for i in range(len(Data)):
#         if Data[i][0] < Data[i][1] and Data[i][0]<Data[i][2] and Data[i][0]<Data[i][3]:
#             shuju1.append(list(dataMat[i]))
#         elif Data[i][1] < Data[i][0] and Data[i][1]<Data[i][2] and Data[i][1]<Data[i][3]:
#             shuju2.append(list(dataMat[i]))
#         elif Data[i][2] < Data[i][0] and Data[i][2]<Data[i][1] and Data[i][2]<Data[i][3]:
#             shuju3.append(list(dataMat[i]))
#         elif Data[i][3] < Data[i][0] and Data[i][3]<Data[i][2] and Data[i][3]<Data[i][1]:
#             shuju4.append(list(dataMat[i]))
#     print(shuju1)
#     print(shuju2)
#     print(shuju3)
#     print(shuju4)
#     # shuju1 正常
#     # shuju2 速率问题 问题1
#     # shuju3 接入耗时问题 问题2
#     # shuju4 漫游达标率问题 问题3
#     global queList
#     for i in range(4):
#         rdata = random.randrange(1, 30)
#         hdata = random.randrange(1, 24)
#         mdata = random.randrange(1, 60)
#         sdata = random.randrange(1, 60)
#         # 问题1的字典
#         que1Dict = {'problemType': 'AP上传速率出现异常',
#                     'deviceRole': 'AR3200',
#                     'problem': shuju2[i][0],
#                     'lastTime': f'2021/8/{rdata} {hdata}:{mdata}:{sdata}',
#                     }
#         # 问题2的字典
#
#         que2Dict = {'problemType': '接入耗时过久',
#                     'deviceRole': 'AR120',
#                     'problem': shuju3[i][2],
#                     'lastTime': f'2021/8/{rdata} {hdata}:{mdata}:{sdata}',
#                     }
#         # 问题3的字典
#
#         que3Dict = {'problemType': '漫游达标率过低',
#                     'deviceRole': 'AR160',
#                     'problem': shuju4[i][3],
#                     'lastTime': f'2021/8/{rdata} {hdata}:{mdata}:{sdata}',
#                     }
#         num = random.randrange(1, 4)
#         if num is 1:
#             queList.append(que1Dict)
#             queList.append(que2Dict)
#         elif num is 2:
#             queList.append(que2Dict)
#             queList.append(que3Dict)
#         else:
#             queList.append(que1Dict)
#             queList.append(que3Dict)
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
dataMat = loadDataSet('text.txt')  # 提取数据集
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



print(queList)