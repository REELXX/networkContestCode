import numpy as np
import matplotlib.pyplot as plt

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
def main():
    #生成高斯分布的随机点
    means1 = [32,89.2,21,33,45,44]
    cov1 = np.eye(6) * 2
    means2 = [100,89.2,21,33,45,44]
    cov2 = np.eye(6) * 2
    means3 = [32,89.2,100,33,45,44]
    cov3 = np.eye(6) * 2
    means4 = [32,89.2,21,0,45,44]
    cov4 = np.eye(6) * 2
    data1 = np.random.multivariate_normal(means1, cov1, 100)
    data2 = np.random.multivariate_normal(means2, cov2, 100)
    data3 = np.random.multivariate_normal(means3, cov3, 100)
    data4 = np.random.multivariate_normal(means4, cov4, 100)
    data = np.vstack((data1,data2,data3,data4))
    U,C = fcm(20,len(data),2,data)
    #dataMat = loadDataSet('text.txt')   #提取数据集
    dataMat = [[32.24277586, 88.00280528, 20.57829836, 31.74397164, 43.75964395, 42.43778038], [29.98704003, 90.34754347, 21.97877372, 33.31555032, 44.25127479, 44.87037341], [31.47028282, 88.87690192, 18.74858385, 33.19088776, 44.96072857, 44.86733174], [32.154147, 88.0174189, 20.75032569, 32.8308963, 47.80965206, 43.46530213], [32.98047896, 90.28955095, 20.48190384, 31.00377041, 43.74474885, 46.34298369], [100.22427249, 89.66891903, 19.49586265, 33.30366252, 44.84399543, 44.38620439], [98.91386345, 86.88619333, 21.15653264, 34.85350047, 45.20070367, 44.34336512], [98.6438615, 89.09825824, 21.15803034, 34.44882292, 44.85170896, 44.19793814], [100.76248192, 87.88341751, 20.6107849, 34.35669861, 46.28748639, 42.00307811], [101.59526755, 91.9637862, 20.3444201, 34.36086199, 46.3218226, 45.24131951], [101.41787933, 86.01723063, 22.12335837, 34.65944799, 44.40702234, 43.25655351], [32.84594444, 88.37563786, 100.96859151, 31.72708431, 45.1863847, 44.01721562], [30.02053272, 92.29890679, 101.2051303, 32.66914331, 44.86670786, 43.41566105], [29.96851861, 89.92184147, 98.060783, 34.05759969, 43.41425224, 41.85408797], [34.59479743, 89.06386419, 100.51903813, 35.1457628, 46.39851924, 43.86783592], [32.80846435, 90.41754888, 99.17201153, 30.49668114, 43.56561671, 43.9894182], [30.23523581, 90.20371509, 20.16209673, 9.23829465, 40.62672765, 40.55022952], [30.20087147, 80.98712676, 10.98851073, 2.47711841, 40.47414021, 40.52840054], [30.29394596, 90.19071149, 10.7752872, 1.29141783, 40.39666337, 40.3776614], [30.51073738, 80.84345879, 20.27158386, 7.08289937, 40.69193309, 40.51524089], [30.15953653, 90.00119612, 20.27342338, 1.89773744, 40.29511474, 40.3046079]]
    dataMat = np.array(dataMat)
    shuju1,shuju2,shuju3,shuju4 = [],[],[],[]
    Data = [[float(0) for q in range(len(C))] for p in range(len(dataMat))]
    for i in range(len(dataMat)):
        for j in range(len(C)):
            dis = ((dataMat[i][0]-C[j][0])**2+(dataMat[i][1]-C[j][1])**2+(dataMat[i][1]-C[j][1])**2+(dataMat[i][2]-C[j][2])**2+(dataMat[i][3]-C[j][3])**2+(dataMat[i][4]-C[j][4])**2+(dataMat[i][5]-C[j][5])**2)**0.5
            Data[i][j] = dis
    Data = np.array(Data)
    for i in range(len(Data)):
        if Data[i][0] < Data[i][1] and Data[i][0]<Data[i][2] and Data[i][0]<Data[i][3]:
            shuju1.append(list(dataMat[i]))
        elif Data[i][1] < Data[i][0] and Data[i][1]<Data[i][2] and Data[i][1]<Data[i][3]:
            shuju2.append(list(dataMat[i]))
        elif Data[i][2] < Data[i][0] and Data[i][2]<Data[i][1] and Data[i][2]<Data[i][3]:
            shuju3.append(list(dataMat[i]))
        elif Data[i][3] < Data[i][0] and Data[i][3]<Data[i][2] and Data[i][3]<Data[i][1]:
            shuju4.append(list(dataMat[i]))
    print(shuju1)
    print(shuju2)
    print(shuju3)
    print(shuju4)



if __name__ == '__main__':
    main()