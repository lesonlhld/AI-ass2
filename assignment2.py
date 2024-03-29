import matplotlib.pyplot as pl
import numpy as np
import math
import random
import time

# Hàm tính công cho mỗi đơn hàng
def caculateEarningsEachOrderItem(v, m):
    return 5 + v + m * 2

# Hàm tính chi phí của mối nhân viên
def caculateCostOfEachSalesman(distance):
    return distance / 40 * 20 + 10

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
def caculateMinimize(deplot, orders, cluster, smanOld = None, profitOld = None):
    profit = {} if smanOld == None else profitOld
    minimize = 0
    if smanOld == None:
        for sman in cluster:
            profit[sman] = caculateProfitOfEachSaleman(sman, 
            cluster, orders, deplot)
    else:
        profit[smanOld] = caculateProfitOfEachSaleman(smanOld, cluster, orders, deplot)
    for sman in cluster:
        for nsman in cluster:
            minimize += abs(profit[sman] - profit[nsman])
    return minimize / 2, profit

# Hàm tính khoảng cách giữa 2 điểm tọa độ của 2 đơn hàng
def distanceBetweenTwoPoints(P1, P2):
    return np.sqrt((P1[0]-P2[0])**2+(P1[1]-P2[1])**2)

# Hàm tính tổng quãng đường mà nhân viên giao hàng cần đi từ kho
def totalDistanceForEachCluster(sman, cluster, deplot):
    dist = 0
    clusterdist = [deplot]
    clusterdist += list(cluster[sman][x]["pos"] for x in cluster[sman])

    for i in range(len(cluster[sman])):
        dist += distanceBetweenTwoPoints(clusterdist[i], clusterdist[i+1])
    return dist

# # Hàm vẽ biểu đồ đường đi giao hàng từ kho của các nhân viên
# def Ploteachcluster(cluster, deplot):
#     pl.title('Lo trinh cua cac nhan vien giao hang')
#     pl.grid()
#     pl.xlim(xmin=0, xmax=maxX + 5)
#     pl.ylim(ymin=0, ymax=maxY + 5)

#     for sman in cluster:
#         # Vị trí đầu tiên bắt đầu từ kho
#         Pt = [deplot]
#         # Các vị trí tiếp theo của các đơn hàng
#         Pt += list(cluster[sman][x]["pos"] for x in cluster[sman])
#         pos = [list(x) for x in set(tuple(i) for i in Pt)]
#         Pt = np.array(Pt)

#         pl.plot(Pt[:,0],Pt[:,1],marker='o')
#         for x in pos:
#             pl.text(x[0],x[1]+0.25,"("+str(x[0]) + ", " + str(x[1]) +")", transform= pl.gca().transData, horizontalalignment = 'center' )

#     pl.show()

# Hàm tạo danh sách đơn hàng cho từng nhân viên giao hàng
def makeSolution(deplot, orders, numOfSalesman):
    # Danh sách kết quả các đơn hàng của từng nhân viên với key là id của nhân viên đó
    solution = {}
    # Kết quả tối ưu lợi nhuận giữa các nhân viên
    minimize = 99999999
    numOfOrders = len(orders)

    # Giới hạn số lần lặp
    temperature = 1e+10
    cooling_rate = 0.975
    temperature_end = 0.0000000001
    begin = time.time()

    # Danh sách tạm thời các đơn hàng của từng nhân viên với key là id của các nhân viên
    cluster = {}
    while (temperature > temperature_end):
        for key in range(numOfSalesman):
            cluster[key] = {}

        # Random số đơn hàng cho mỗi nhân viên
        order = list(range(numOfOrders))
        a = random.sample(range(1, numOfOrders), numOfSalesman - 1) + [0, numOfOrders]
        list.sort(a)
        b = [a[i+1] - a[i] for i in range(len(a) - 1)]

        # Thực hiện gán đơn hàng cho nhân viên
        for i in range(numOfSalesman):
            # Chọn đơn hàng bất kỳ
            for j in range(b[i]):
                x = order.pop(random.randrange(len(order)))
                cluster[i][str(x)] = orders[str(x)]
                
        # Hàm tối ưu lộ trình cho các nhân viên giao hàng
        tempCluster, tempMinimize = makeBestSolution(
            deplot, orders, cluster, minimize)

        # Kết quả tối ưu lợi nhuận giữa các nhân viên với vị trí hiện tại và sau khi tối ưu lộ trình
        if tempMinimize < minimize:
            # Cập nhật kết quả tối ưu
            minimize = tempMinimize
            # Cập nhật danh sách kết quả các đơn hàng của các nhân viên
            solution = dict(tempCluster)

        # Cập nhật điều kiện dừng vòng lặp
        temperature = temperature * cooling_rate
        end = time.time()
        if end - begin > 500:
            break

    # # In danh sách các đơn hàng của từng nhân viên
    # for i in range(numOfSalesman):
    #     print("Nhan vien " + str(i) + ": " + ', '.join(str(x) for x in list(solution.values())[i]))

    # # Kết quả hàm tối ưu hiện tại
    # print("Ket qua sau khi toi uu: " + str(minimize))
    # # Ploteachcluster(solution, deplot)

    # Trả về kết quả
    return solution

# Hàm đổi ngẫu nhiên thứ tự đơn hàng của nhân viên đó
def swap(cluster, nsman):
    # Nếu nhân viên đó có từ 2 đơn hàng trở lên mới đổi được thứ tự các đơn hàng với nhau
    if len(cluster[nsman]) > 1:
        # Lấy ngẫu nhiên 2 đơn hàng trong danh sách
        key1, key2 = np.random.choice(list(cluster[nsman]), 2, replace=False)
        temp1 = cluster[nsman][key1]
        temp2 = cluster[nsman][key2]
        sman = {}
        for x in cluster[nsman]:
            if x == key1:
                sman[key2] = temp2
            elif x == key2:
                sman[key1] = temp1
            else:
                sman[x] = cluster[nsman][x]
        return sman
    return cluster[nsman]

# Hàm tối ưu lộ trình cho các nhân viên giao hàng
def makeBestSolution(deplot, orders, cluster, minimize):
    # Danh sách kết quả mới cho các đơn hàng của từng nhân viên với key là id của nhân viên đó
    solution = dict(cluster)
    # Kết quả tối ưu lợi nhuận mới giữa các nhân viên
    nMinimize, profit = caculateMinimize(deplot, orders, solution)
    

    # print(solution)
    # print("curent = " +str(nMinimize))
    if nMinimize/minimize < 1.2:
        # Giới hạn số lần lặp
        temperature = 1e+10
        cooling_rate = 0.975
        temperature_end = 0.0000000001
        begin = time.time()
        finalCount = 0
        
        while (temperature > temperature_end) and (finalCount < 50):
            # Danh sách tạm thời các đơn hàng của từng nhân viên với key là vị trí của các nhân viên
            newCluster = dict(solution)
            newProfit = dict(profit)

            # Duyệt từng nhân viên
            for sman in solution:
                if len(solution[sman]) > 1:
                    #print("Min1 = " +str(caculateMinimize(deplot,orders,newCluster)))
                    # Đổi ngẫu nhiên thứ tự đơn hàng của nhân viên đó
                    next_order = swap(solution, sman)
                    # Cập nhật thứ tự đơn hàng của nhân viên đó trong danh sách tạm thời các đơn hàng
                    newCluster[sman] = next_order
                    # Kết quả tối ưu lợi nhuận giữa các nhân viên với thứ tự đơn hàng mới
                    tempMinimize, tempProfit = caculateMinimize(deplot, orders, newCluster, sman, newProfit)
                    if tempMinimize < nMinimize:
                        profit = dict(tempProfit)
                        # Cập nhật kết quả tối ưu
                        nMinimize = tempMinimize
                        # Cập nhật danh sách kết quả các đơn hàng của nhân viên đó
                        solution = dict(newCluster)
                        # print(solution)
                        finalCount = 0
                    elif tempMinimize == nMinimize:
                        finalCount += 1

            # Cập nhật điều kiện dừng vòng lặp
            temperature = temperature * cooling_rate
            end = time.time()
            if end - begin > 20:
                break
    return solution, nMinimize


def assign(file_input, file_output):
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
    # Danh sách thông tin các đơn hàng là 1 dictionary với key là Id
    orders = {}

    # Đọc file input và lấy dữ liệu
    with open(file_input) as fp:
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

    # Hàm xử lý
    output = makeSolution(deplot, orders, numOfSalesman)

    # Ghi kết quả ra file
    solution = open(file_output, "w")
    for i in range(numOfSalesman):
        solution.write(' '.join(str(x) for x in list(output.values())[i]))
        if i != (numOfSalesman - 1):
            solution.write('\n')
    solution.close()
    # print(caculateMinimize(deplot,orders,output)[0])


# if __name__ == "__main__":
#     assign('input.txt', 'output.txt')
