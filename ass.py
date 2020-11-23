import matplotlib.pyplot as pl
import numpy as np
import math

def randomPositionOfSalesman(numOfSalesman):
    S = []
    for i in range(numOfSalesman):
        s1 = np.random.randint(1, maxX)
        s2 = np.random.randint(1, maxY)
        S.append([s1, s2])
    return S

def caculateEarningsEachOrderItem(orderItem):
    v, m = orderItem
    return 5 + v + m * 2

def caculateCostOfEachSalesman(distance):
    return distance / 40 *20 + 10

def caculateSalaryOfEachSalesman(order, sman, cluster):
    salary = 0
    for x in cluster[sman]:
        salary += cluster[sman][x]["e"] 
    return salary

def caculateProfitOfEachSaleman(sman, cluster, orderItem, deplot):
    distance = totalDistanceForEachCluster(sman, cluster, deplot)
    cost = caculateCostOfEachSalesman(distance)
    salary = caculateSalaryOfEachSalesman(orderItem, sman, cluster)
    profit = salary - cost
    return profit

def caculateMinimize(cluster, orders):
    distance = {}
    cost = {}
    salary = {}
    profit = {}
    minimize = 0
    for sman in cluster:
        distance[sman] = totalDistanceForEachCluster(sman, cluster, deplot)
        cost[sman] = caculateCostOfEachSalesman(distance[sman])
        salary[sman] = caculateSalaryOfEachSalesman(orders, sman, cluster)
        profit[sman] = salary[sman] - cost[sman]
    for sman in cluster:
        for nsam in cluster:
            minimize += abs(profit[sman] - profit[nsam])
    return minimize / 2

def distanceBetweenTwoPoints(P1, P2):
    return np.sqrt((P1[0]-P2[0])**2+(P1[1]-P2[1])**2)

def totalDistanceForEachCluster(sman, cluster, deplot):
    dist = 0
    clusterdist = [deplot]
    clusterdist += list(cluster[sman][x]["pos"] for x in cluster[sman])

    for i in range(len(cluster[sman])):
        dist+=distanceBetweenTwoPoints(clusterdist[i],clusterdist[i+1])
    return dist

def Ploteachcluster(cluster, distance, deplot):
    colours = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']
    k=0

    # p1 = pl.Rectangle((0,0),0.1,0.1,fc=colours[0])
    # p2 = pl.Rectangle((0,0),0.1,0.1,fc=colours[1])
    # p3 = pl.Rectangle((0,0),0.1,0.1,fc=colours[2])
    # p4 = pl.Rectangle((0,0),0.1,0.1,fc=colours[3])
    # p5 = pl.Rectangle((0,0),0.1,0.1,fc=colours[4])
    # pl.legend((p1,p2,p3,p4,p5),('Salesman1','Salesman2','Salesman3','Salesman4','Salesman5'),loc='center right')


    pl.title('Total distance=' + str(distance))
    pl.xlim(xmin=-5,xmax=maxX + 5)
    pl.ylim(ymin=-5,ymax=maxY + 5)

    for sman in cluster:
        Pt = [deplot]
        # Pt = [sman]
        Pt += list(cluster[sman][x]["pos"] for x in cluster[sman])
        Pt = np.array(Pt)

        pl.plot(Pt[:,0],Pt[:,1],marker='o',c=colours[k])
        k+=1

    pl.show()

# Hàm tạo danh sách đơn hàng cho từng nhân viên giao hàng
def kmeans(deplot, orders, numOfSalesman):
    # Danh sách kết quả các đơn hàng của từng nhân viên với key là vị trí của nhân viên đó
    solution = {}
    # Kết quả tối ưu lợi nhuận giữa các nhân viên
    minimize = 99999999

    # Giới hạn số lần lặp
    temperature = 1e+10
    cooling_rate = 0.85
    temperature_end = 0.0000000001

    while temperature > temperature_end:
        # Tạo random vị trí cho từng nhân viên
        t = randomPositionOfSalesman(numOfSalesman)
        positionOfSalesman = list(set(tuple(i) for i in t))
        print((positionOfSalesman))
        # Nếu có nhiều nhân viên cùng 1 vị trí thì quay lại random vị trí khác cho các nhân viên
        if len(positionOfSalesman) < numOfSalesman:
            continue
        # Danh sách tạm thời các đơn hàng của từng nhân viên với key là vị trí của các nhân viên
        cluster = {}
        for x in range(numOfSalesman):
            key = tuple(positionOfSalesman[x])
            cluster[key] = {}
        
        

        # Thực hiện gán từng đơn hàng cho nhân viên với tiêu chí đơn hàng đó gần nhân viên nào nhất
        for i in orders:
            # Khoảng cách ngắn nhất của đơn hàng này đến nhân viên gần nhất
            min = 99999999
            # Tọa độ nhân viên gần nhất
            pos = []
            # Duyệt từng nhân viên
            for j in range(numOfSalesman):
                if(min > distanceBetweenTwoPoints(orders[i]["pos"],positionOfSalesman[j])):
                    # Cập nhật khoảng cách ngắn nhất
                    min = distanceBetweenTwoPoints(orders[i]["pos"],positionOfSalesman[j])
                    # Cập nhật tọa độ nhân viên gần nhất
                    pos = positionOfSalesman[j]

            # Lấy danh sách đơn hàng của nhân viên gần nhất
            tmp_arr = cluster[tuple(pos)]
            # Thêm đơn hàng này vào danh sách đơn hàng của nhân viên đó
            tmp_arr[i] = orders[i]
            # Cập nhật danh sách đơn hàng cho nhân viên đó và qua đơn hàng tiếp theo
            cluster[tuple(pos)] = tmp_arr

        # Nếu tồn tại 1 nhân viên nào đó không có đơn hàng nào thì quay lại random vị trí khác cho các nhân viên
        if ({} in cluster.values()):
            continue
        # Ngược lại, tính toán các giá trị cho từng nhân viên với danh sách đơn hàng mà họ có
        else:
            # Quãng đường mà nhân viên phải di chuyển đi giao hàng
            distance = {}
            # Chi phí của mối nhân viên
            cost = {}
            # Lợi nhuận của mỗi nhân viên
            salary = {}
            # Duyệt từng nhân viên và tính toán các giá trị trên cho mỗi nhân viên
            for sman in cluster:
                distance[sman] = totalDistanceForEachCluster(sman, cluster, deplot)
                cost[sman] = caculateCostOfEachSalesman(distance[sman])
                salary[sman] = caculateSalaryOfEachSalesman(orders, sman, cluster)

            # Nếu có nhân viên nào có lợi nhuận âm thì quay lại random vị trí khác cho các nhân viên
            for sman in cluster:
                if salary[sman] < cost[sman]:
                    continue
        
        # Kết quả tối ưu lợi nhuận giữa các nhân viên với vị trí hiện tại
        nMnimize = caculateMinimize(cluster, orders)
        if minimize > nMnimize:
            # Cập nhật kết quả tối ưu
            minimize = nMnimize
            # Cập nhật danh sách tối ưu các đơn hàng của các nhân viên
            solution = dict(cluster)
        # Cập nhật điều kiện dừng vòng lặp
        temperature = temperature * cooling_rate

    # In danh sách tối ưu các đơn hàng của từng nhân viên
    for sman in solution:
        print(str(sman) + ": " + str(solution[sman]))
        # print("Doanh thu: " + str(salary[sman]))
        # print("Quang duong: " + str(distance[sman]))
        # print("Chi phi: " + str(cost[sman]))
        # print("Loi nhuan: " + str(salary[sman] - cost[sman]))

    # Kết quả hàm tối ưu hiện tại
    print("Truoc toi uu: " + str(caculateMinimize(solution, orders)))
    # Ploteachcluster(cluster, distance, deplot)
    print("-----------------------------")

    # Hàm tối ưu lộ trình cho nhân viên giao hàng
    SA_new(deplot, orders, positionOfSalesman, solution)

def swap(cluster, nsman):
    if len(cluster[nsman]) == 2:
        key1, key2 = np.random.choice(list(cluster[nsman]), 2,replace=False)
        temp1 = cluster[nsman][key1]
        temp2 = cluster[nsman][key2]
        # print(str(nsman) + "==========================")
        # print([key1, key2])
        # print(cluster[nsman])
        sman = {}
        for x in cluster[nsman]:
            if x == key1:
                sman[key2]=temp2
            elif x == key2:
                sman[key1]=temp1
            else:
                sman[x] = cluster[nsman][x]
        cluster[nsman] = dict(sman)
        # print(cluster[nsman])
        # print(str(nsman) + "==========================")

    elif len(cluster[nsman]) > 2:
        key1, key2 = np.random.choice(list(cluster[nsman]), 2,replace=False)
        key3, key4 = np.random.choice(list(cluster[nsman]), 2,replace=False)
        temp1 = cluster[nsman][key1]
        temp2 = cluster[nsman][key2]
        temp3 = cluster[nsman][key3]
        temp4 = cluster[nsman][key4]
        # print(str(nsman) + "==========================")
        # print([key1, key2, key3, key4])
        # print(cluster[nsman])
        sman = {}
        for x in cluster[nsman]:
            if x == key1:
                sman[key2]=temp2
            elif x == key2:
                sman[key1]=temp1
            else:
                sman[x] = cluster[nsman][x]
        cluster[nsman] = dict(sman)
        sman = {}
        for x in cluster[nsman]:
            if x == key3:
                sman[key4]=temp4
            elif x == key4:
                sman[key3]=temp3
            else:
                sman[x] = cluster[nsman][x]
        cluster[nsman] = dict(sman)

        # print(cluster[nsman])
        # print(str(nsman) + "==========================")

    return cluster[nsman]


def SA_new(deplot, orders, positionOfSalesman, cluster):
    new_cluster = {}
    solution = dict(cluster)
    mintotal = 0;

    for x in range(0,len(positionOfSalesman)):
         key = tuple(positionOfSalesman[x])
         new_cluster[key] = {}

    count=0

    temperature = 1e+10
    cooling_rate = 0.85
    temperature_end = 0.0000000001

    while temperature > temperature_end:
        count +=1

        #print (count)
        for nsman in cluster:
            minimize = caculateMinimize(cluster, orders)

            next_order = swap(cluster, nsman)
            """next_order = np.random.permutation(cluster[nsman])"""

            new_cluster[nsman] = next_order

            nMinimize = caculateMinimize(new_cluster, orders)
            #print ("total distance is " + str(dist_new), nsman)

            difference = nMinimize - minimize

            # if difference < 0 or math.e**(-difference/temperature) > np.random.rand():
            if difference < 0:

                solution[nsman] = new_cluster[nsman]
                mintotal = nMinimize

                # """print( "solution is " + str(solution))"""
                # final_dist = dist_new
                # print ("final total distance is " + str(final_dist), nsman)
                # """Ploteachcluster(solution,final_dist)"""

            temperature = temperature * cooling_rate

    """Ploteachcluster(solution,final_dist)"""
    distance = {}
    cost = {}
    salary = {}
    for nsman in solution:
        distance[nsman] = totalDistanceForEachCluster(nsman, solution, deplot)
        cost[nsman] = caculateCostOfEachSalesman(distance[nsman])
        salary[nsman] = caculateSalaryOfEachSalesman(orders, nsman, solution)

    for nsman in solution:
        print(str(nsman) + ": " + str(solution[nsman]))
        # print("Doanh thu: " + str(salary[nsman]))
        # print("Quang duong: " + str(distance[nsman]))
        # print("Chi phi: " + str(cost[nsman]))
        # print("Loi nhuan: " + str(salary[nsman] - cost[nsman]))
    # print(solution)
    distance=list(distance.values())
    print("Sau toi uu: " + str(caculateMinimize(solution, orders)))
    Ploteachcluster(solution, distance, deplot)


if __name__=='__main__':
    # numOfOrders = 8
    # numOfSalesman = 3
    # maxX = 10
    # maxY = 10
    # # Deplot
    # deplot = [5, 5]

    # orders = {}
    # for i in range(numOfOrders):
    #     orderItem = {}
    #     x=np.random.randint(1,maxX)
    #     y=np.random.randint(1,maxY)
    #     orderItem["pos"] = [x,y]
    #     v=np.random.randint(1,5)
    #     orderItem["v"] = v
    #     m=np.random.randint(1,5)
    #     orderItem["m"] = m
    #     orderItem["e"] = caculateEarningsEachOrderItem([v, m])
    #     orders[str(i)]=orderItem

    # print("Orders are " + str(list([orders[x]["pos"] for x in orders])))
    # print("Details are " + str(list([[orders[x]["v"], orders[x]["m"]] for x in orders])))

    # # orders = np.array(orders)

    # kmeans(deplot, orders, numOfSalesman)
    """---------------------------------------------------------------------------------------"""

    # Số đơn hàng
    numOfOrders = 0
    # Số nhân viên giao hàng
    numOfSalesman = 0
    # Tọa độ đơn hàng nhỏ nhất và lớn nhất
    minX = 0
    maxX = 0
    minY = 0
    maxY = 0
    # Tọa độ kho
    deplot = []
    # Id đơn hàng
    Id = 0
    # Danh sách thông tin các đơn hàng là 1 dictionary với key là Id
    orders = {}

    # Đọc file input và lấy dữ liệu
    with open("input.txt") as fp:
        # Tách các dòng thành 1 danh sách
        Lines = fp.read().split('\n')
        # Lấy vị trí kho ở dòng đầu tiên
        deplot = [int(x) for x in Lines[0].split(' ')]
        # Lấy số lượng nhân viên và đơn hàng ở dòng thứ 2
        numOfSalesman, numOfOrders = [int(x) for x in Lines[1].split(' ')]
        # Lấy thông tin từng đơn hàng
        for line in Lines[2:]:
            # Tách thông tin đơn hàng thành 1 list
            line = line.split(' ')
            # Thông tin đơn hàng được lưu trong 1 dictionary
            orderItem = {}
            # Lấy tọa độ của đơn hàng
            x = int(line[0])
            minX = x if x < minX else minX
            maxX = x if x > maxX else maxX
            y = int(line[1])
            minY = y if y < minY else minY
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
            orderItem["e"] = caculateEarningsEachOrderItem([v, m])
            # Lưu thông tin đơn hàng vào danh sách các đơn hàng với key là Id
            orders[str(Id)] = orderItem
            # Tăng Id lên 1 đơn vị cho đơn hàng tiếp theo
            Id += 1

    # In tọa độ các đơn hàng
    print("Orders are " + str(list([orders[x]["pos"] for x in orders])))
    # In thông tin về thể tích và tkhối lượng từng đơn hàng tương ứng
    print("Details are " + str(list([[orders[x]["v"], orders[x]["m"]] for x in orders])))

    # Hàm xử lý
    kmeans(deplot, orders, numOfSalesman)