import numpy as np
import os
from assignment2 import assign
import time
from datetime import datetime

# Hàm tạo testcase
def genTest(filename):
    # Số đơn hàng
    numOfOrders = np.random.randint(5,100)
    # Số nhân viên giao hàng
    numOfSalesman = np.random.randint(1,numOfOrders)
    # Tọa độ đơn hàng nhỏ nhất và lớn nhất
    maxX = 20
    maxY = 20
    # Tọa độ kho
    x=np.random.randint(5,maxX-5)
    y=np.random.randint(5,maxY-5)

    # Ghi testcase ra file
    fo = open(filename, "w")
    fo.write(str(x) + " " + str(y) + "\n")
    fo.write(str(numOfOrders) + " " + str(numOfSalesman) + "\n")

    for i in range(numOfOrders):
        x=np.random.randint(1,maxX)
        y=np.random.randint(1,maxY)
        v=np.random.randint(1,5)
        m=np.random.randint(1,5)
        fo.write(str(x) + " " + str(y) + " " + str(v) + " " + str(m))
        if i != (numOfOrders - 1):
            fo.write('\n')

# Hàm tính khoảng cách giữa 2 điểm tọa độ của 2 đơn hàng
def distanceBetweenTwoPoints(P1, P2):
    return np.sqrt((P1[0]-P2[0])**2+(P1[1]-P2[1])**2)

# Hàm tính tổng quãng đường mà nhân viên giao hàng cần đi từ kho
def totalDistanceForEachCluster(sman, cluster, deplot):
    dist = 0
    clusterdist = [deplot]
    clusterdist += list(cluster[sman][x]["pos"] for x in cluster[sman])

    for i in range(len(cluster[sman])):
        dist+=distanceBetweenTwoPoints(clusterdist[i],clusterdist[i+1])
    return dist

# Hàm tính công cho mỗi đơn hàng
def caculateEarningsEachOrderItem(v, m):
    return 5 + v + m * 2

# Hàm tính chi phí của mối nhân viên
def caculateCostOfEachSalesman(distance):
    return distance / 40 *20 + 10

# Hàm tính doanh thu cho mỗi nhân viên với danh sách đơn hàng mà họ được gán
def caculateSalaryOfEachSalesman(orders, sman, cluster):
    salary = 0
    for x in cluster[sman]:
        salary += cluster[sman][x]["e"] 
    return salary

# Hàm tính lợi nhuận của mỗi nhân viên
def caculateProfitOfEachSaleman(sman, cluster, orders, deplot):
    distance = totalDistanceForEachCluster(sman, cluster, deplot)
    cost = caculateCostOfEachSalesman(distance)
    salary = caculateSalaryOfEachSalesman(orders, sman, cluster)
    profit = salary - cost
    return profit

# Hàm tính tổng chênh lệch lợi nhuận giữa các nhân viên
def caculateMinimize(deplot, orders, cluster):
    profit = {}
    minimize = 0
    for sman in cluster:
        profit[sman] = caculateProfitOfEachSaleman(sman, cluster, orders, deplot)
    for i in cluster:
        for j in cluster:
            minimize += abs(profit[i] - profit[j])
    # return minimize / 2
    return minimize

# Hàm tính tổng chênh lệch lợi nhuận giữa các nhân viên dựa trên kết quả file output
def caculateSolution(filename, deplot, orders, numOfSalesman):
    solution = {}
    with open(filename) as fp:
        # Tách các dòng thành 1 danh sách
        Lines = fp.read().split('\n')
        for key in range(numOfSalesman):
            solution[str(key)] = {}
            # Tách danh sách đơn hàng thành 1 list
            line = Lines[key].split(' ')
            for x in line:
                solution[str(key)][x] = orders[x]
    minimize = caculateMinimize(deplot, orders, solution)
    return minimize


if __name__=='__main__':
    # if not os.path.isfile("input.txt"):
    #     genTest("input.txt")
    log = open("Log.txt", "a")
    log.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
    for j in range(1):
        for i in range(1, 26):
            print("Testcase " + str(i))
            log.write("Testcase " + str(i) + "\n")
            inputFile = str(i) + ".txt"
            outputFile = str(i) + "_.txt"
            resultFile = "result_" + str(i) + ".txt"
            # genTest(inputFile)

            # Số đơn hàng
            numOfOrders = 0
            # Số nhân viên giao hàng
            numOfSalesman = 0
            # Tọa độ đơn hàng lớn nhất
            maxX = 0
            maxY = 0
            # Tọa độ kho
            deplot = []
            # Id đơn hàng
            Id = 0
            minimize = 0
            # Danh sách thông tin các đơn hàng là 1 dictionary với key là Id
            orders = {}

            # Đọc file input và lấy dữ liệu
            with open(inputFile) as fp:
                # Tách các dòng thành 1 danh sách
                Lines = fp.read().split('\n')
                # Lấy vị trí kho ở dòng đầu tiên
                deplot = [int(x) for x in Lines[0].split(' ')]
                # Lấy số lượng nhân viên và đơn hàng ở dòng thứ 2
                numOfOrders, numOfSalesman = [int(x) for x in Lines[1].split(' ')]
                # Lấy thông tin từng đơn hàng
                for line in Lines[2:2+numOfOrders]:
                    # Tách thông tin đơn hàng thành 1 list
                    line = line.split(' ')
                    # Thông tin đơn hàng được lưu trong 1 dictionary
                    orderItem = {}
                    # Lấy tọa độ của đơn hàng
                    x = int(line[0])
                    maxX = x if x > maxX else maxX
                    y = int(line[1])
                    maxY = y if y > maxY else maxY
                    # Lưu tọa độ với key là pos
                    orderItem["pos"] = [x, y]
                    # Lấy thông tin thể tích và lưu với key là v
                    v = int(line[2])
                    orderItem["v"] = v
                    # Lấy thông tin khối lượng và lưu với key là m
                    m = int(line[3])
                    orderItem["m"] = m
                    # Tính công cho mỗi đơn hàng và lưu với key là e
                    orderItem["e"] = caculateEarningsEachOrderItem(v, m)
                    # Lưu thông tin đơn hàng vào danh sách các đơn hàng với key là Id
                    orders[str(Id)] = orderItem
                    # Tăng Id lên 1 đơn vị cho đơn hàng tiếp theo
                    Id += 1
                    
            begin = time.time()
            assign(inputFile, outputFile)
            end = time.time()
            timeRun = end - begin
            print("Time run: " + str(timeRun))
            log.write("Time run: " + str(timeRun) + "\n")

            nMinimize = caculateSolution(outputFile, deplot, orders, numOfSalesman)
            print("Current Minimize: " + str(nMinimize))
            log.write("Current Minimize: " + str(nMinimize) + "\n")
            
            if os.path.isfile(resultFile):
                minimize = caculateSolution(resultFile, deplot, orders, numOfSalesman)
                print("Previous Minimize: " + str(minimize))
                log.write("Previous Minimize: " + str(minimize) + "\n")
                if nMinimize < minimize:
                    os.remove(resultFile)
                    os.rename(outputFile, resultFile)
            else:
                os.rename(outputFile, resultFile)
            if os.path.isfile(outputFile):
                    os.remove(outputFile)
            print("================================")
            log.write("================================\n")
        print("#######################################")
        log.write("\n#######################################\n")
    log.write("\n")
    log.close()