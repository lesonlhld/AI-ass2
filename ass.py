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


def kmeans(deplot, orders, numOfSalesman):
    S = randomPositionOfSalesman(numOfSalesman)
    cluster = {}

    for x in range(0,len(S)):
         key = tuple(S[x])
         cluster[key] = {}

    for i in orders:
        min = 99999999
        min_s = []
        for j in range(len(S)):
            if(min > distanceBetweenTwoPoints(orders[i]["pos"],S[j])):
                min = distanceBetweenTwoPoints(orders[i]["pos"],S[j])
                min_s = S[j]
                min_r = i

        tmp_arr = cluster[tuple(min_s)]
        tmp_arr[min_r] = orders[i]
        cluster[tuple(min_s)] = tmp_arr
    # print(cluster)

    if (len(cluster) < numOfSalesman) or ({} in cluster.values()):
        kmeans(deplot, orders, numOfSalesman)
    else:
        distance = {}
        cost = {}
        salary = {}
        for sman in cluster:
            distance[sman] = totalDistanceForEachCluster(sman, cluster, deplot)
            cost[sman] = caculateCostOfEachSalesman(distance[sman])
            salary[sman] = caculateSalaryOfEachSalesman(orders, sman, cluster)

        # print(distance)
        # print(cost)
        # print(salary)
            
        check = False
        for sman in cluster:
            if salary[sman] < cost[sman]:
                check = True
                kmeans(deplot, orders, numOfSalesman)
                break

        # if check == False:
        #     salesman = list(cluster.keys())
        #     profit = [salary[x] - cost[x] for x in salesman]
        #     print(profit)
        #     while abs(profit[0] - profit[1]) > 3.5 or abs(profit[0] - profit[2]) > 3.5 or abs(profit[2] - profit[1]) > 3.5:
        #         check = True
        #         kmeans(deplot, orders)
        #         break

        if check == False:
            for sman in cluster:
                print(str(sman) + ": " + str(cluster[sman]))
                # print("Doanh thu: " + str(salary[sman]))
                # print("Quang duong: " + str(distance[sman]))
                # print("Chi phi: " + str(cost[sman]))
                # print("Loi nhuan: " + str(salary[sman] - cost[sman]))
            distance=list(distance.values())
            print("Truoc toi uu: " + str(caculateMinimize(cluster, orders)))
            # Ploteachcluster(cluster, distance, deplot)
            print("-----------------------------")
            SA_new(deplot, orders, S, cluster)

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


def SA_new(deplot, orders, S, cluster):
    new_cluster = {}
    solution = dict(cluster)
    mintotal = 0;

    for x in range(0,len(S)):
         key = tuple(S[x])
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
    
    numOfOrders = 0
    numOfSalesman = 0
    maxX = 0
    maxY = 0
    deplot = []
    orders = {}
    with open("input.txt") as fp: 
        Lines = fp.read().split('\n')
        deplot = [int(x) for x in Lines[0].split(' ')]
        numOfSalesman, numOfOrders = [int(x) for x in Lines[1].split(' ')]
        count = 0
        for line in Lines[2:]:
            line = line.split(' ')
            orderItem = {}
            x = int(line[0])
            maxX = x if x > maxX else maxX
            y = int(line[1])
            maxY = x if x > maxY else maxY
            orderItem["pos"] = [x,y]
            v = int(line[2])
            orderItem["v"] = v
            m = int(line[3])
            orderItem["m"] = m
            orderItem["e"] = caculateEarningsEachOrderItem([v, m])
            orders[str(count)]=orderItem
            count += 1

    print("Orders are " + str(list([orders[x]["pos"] for x in orders])))
    print("Details are " + str(list([[orders[x]["v"], orders[x]["m"]] for x in orders])))

    kmeans(deplot, orders, numOfSalesman)