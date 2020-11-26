import heapq
import copy
import numpy as np
import time

class priorityQueue:
    def __init__(self):
        self.cities = []

    def push(self, city, cost):
        heapq.heappush(self.cities, (cost, city))

    def pop(self):
        return heapq.heappop(self.cities)[1]

    def isEmpty(self):
        if (self.cities == []):
            return True
        else:
            return False

    def check(self):
        print(self.cities)


def astar(start, end, maxHeapOrders):
    numOfSalesman = len(start)
        #path = {}
        #distance = {}
    q = priorityQueue()
        #h = makehuristikdict()
        # q là open list là min heap với f(n) = g(n) + h(n)
    q.push(start, 0) # push thành phố đầu tiên vào heap open list (với chi phí thấp nhất)
        #distance[start] = 0 # khoảng cách từ start đến thành phố đó
        #path[start] = None # thành phố cần đến trước thành phố này
    expandedList = []
    
    while (q.isEmpty() == False):
        current = q.pop()
        expandedList.append(current) # expandedList là danh sách các city đã duyệt
        if (countDeliveredList(current) == end):
            break
        newOrder = []
            #print(maxHeapOrders.check())
        for i in range(countDeliveredList(current) - (numOfSalesman - 1)):
            newOrder.append(maxHeapOrders.pop())
        newOrder2 = copy.deepcopy(newOrder[-1])
        for i in range(countDeliveredList(current) - (numOfSalesman - 1)):
            maxHeapOrders.push(newOrder[i], -1 * newOrder[i]['e'])
            #print(maxHeapOrders.check())
            #print(newOrder2)
        childrenOfCurrent = {}
        for i in range(numOfSalesman):
            childrenOfCurrent[i] = copy.deepcopy(current)
            childrenOfCurrent[i][i].append(newOrder2)
            g_cost = caculateMinimize(childrenOfCurrent[i])
                # điều kiện để thêm một node vào open list: 1) nếu node là thành phố mới (mặc dù node mới có thể dài hơn, nhưng node con của node mới có thể ngắn hơn nên phải khám phá), hoặc nếu là node cũ thì đường đi tới node đó ngắn hơn
                #print("node: " + str((childrenOfCurrent[i], g_cost)))
                # nếu thành phố mới này chưa được khám phá hoặc khám phá rồi mà có đường đi đến nó nhỏ hơn
                # thì push nó vào open list
            if (childrenOfCurrent[i] not in expandedList):
                    #f_cost = g_cost + heuristic(new.city, h)
                q.push(childrenOfCurrent[i], g_cost)

    return expandedList


def printoutput(expandedList):
    # for i in expandedList:
    #     print(i)
    #     print(caculateMinimize(i))
    print(expandedList[-1])
    print(caculateMinimize(expandedList[-1]))
    f = open("output.txt", "w")
    for i in expandedList[-1]:
        for j in (expandedList[-1][i]):
            if len(expandedList[-1][i]) == 1:
                f.write(j['name'])
                f.write(' ')
            else:
                f.write(j['name'])
            if j == expandedList[-1][i][-1]:
                f.write('\n')
            else:
                f.write(' ')

    f.close()
    
def caculateEarningsEachOrderItem(orderItem):
    v, m = orderItem
    return 5 + v + m * 2
def countDeliveredList(deliveredList):
    count = 0
    for x in deliveredList:
        count += len(deliveredList[x])
    return count

def totalDistanceForEachCluster(temp):
    dist = 0
    clusterdist = [deplot]
    clusterdist += list(x["pos"] for x in temp)
    for i in range(len(clusterdist) - 1):
         dist+=distanceBetweenTwoPoints(clusterdist[i],clusterdist[i+1])
    return dist

def caculateCostOfEachSalesman(distance):
    return distance / 40 *20 + 10

def caculateSalaryOfEachSalesman(temp):
    salary = 0
    for i in temp:
        salary += i["e"] 
    return salary


def caculateMinimize(temp):
    # danh sách đơn hàng đã giao
    #{0: [{'name': '0', 'pos': [1, 1], 'v': 3, 'm': 4, 'e': 16}, {'name': '2', 'pos': [6, 1], 'v': 3, 'm': 1, 'e': 10}], 1: [{'name': '3', 'pos': [0, 4], 'v': 1, 'm': 3, 'e': 12}], 2: [{'name': '4', 'pos': [7, 5], 'v': 2, 'm': 2, 'e': 11}]}
    distance = {}
    cost = {}
    salary = {}
    profit = {}
    minimize = 0
    for i in temp:
        #print(temp[i])
        distance[i] = totalDistanceForEachCluster(temp[i])
        cost[i] = caculateCostOfEachSalesman(distance[i])
        salary[i] = caculateSalaryOfEachSalesman(temp[i])
        profit[i] = salary[i] - cost[i]
    for i in temp:
         for j in temp:
             minimize += abs(profit[i] - profit[j])
    return minimize / 2
    

def distanceBetweenTwoPoints(P1, P2):
    return np.sqrt((P1[0]-P2[0])**2+(P1[1]-P2[1])**2)

deplot = [] # vị trí kho
def assign2(file_input, file_output):
    # start = src = danh sách đơn hàng ban đầu...#src = "Arad"
    # goal = dst danh sách đơn hàng = 0...#dst = "Bucharest"
    numOfOrders = 0
    numOfSalesman = 0
    global deplot# vị trí kho
    maxX = 0
    maxY = 0
    
    orders = {}
    with open(file_input) as fp:
        Lines = fp.read().split('\n')
        deplot = [int(x) for x in Lines[0].split(' ')]
        numOfSalesman, numOfOrders = [int(x) for x in Lines[1].split(' ')]
        count = 0
        for line in Lines[2:2+numOfOrders]:
            line = line.split(' ')
            orderItem = {}
            x = int(line[0])
            maxX = x if x > maxX else maxX
            y = int(line[1])
            maxY = y if y > maxY else maxY
            orderItem["name"] = str(count)
            orderItem["pos"] = [x,y]
            v = int(line[2])
            orderItem["v"] = v
            m = int(line[3])
            orderItem["m"] = m
            orderItem["e"] = caculateEarningsEachOrderItem([v, m])
            orders[str(count)]=orderItem
            count += 1
        #makedict()
        #print(orders)
    maxHeapOrders = priorityQueue()
    for i in range(numOfOrders):
        maxHeapOrders.push(orders[str(i)], -1 * orders[str(i)]['e'])
    
        # while (maxHeapOrders.isEmpty() == False):
        #      maxHeapOrders.check()
        #      maxHeapOrders.pop()
        

    deliveredList = {}
    for i in range(numOfSalesman):
        deliveredList[i] = [maxHeapOrders.pop()]
    #print(maxHeapOrders.check())
    src = deliveredList
    dst = numOfOrders
    output = astar(src, dst, maxHeapOrders)

    f = open(file_output, "w")
    for i in output[-1]:
        for j in (output[-1][i]):
            if len(output[-1][i]) == 1:
                f.write(j['name'])
            else:
                f.write(j['name'])
            if j == output[-1][i][-1]:
                f.write('\n')
            else:
                f.write(' ')

    f.close()

# class ctNode:
#     def __init__(self, city, distance):
#         self.city = str(city)
#         self.distance = str(distance)


# romania = {}

# # make danh sách những thành phố liền kề với một thành phố nào đó
# def makedict():
#     file = open("romania.txt", 'r')
#     for string in file:
#         line = string.split(',')
#         ct1 = line[0]
#         ct2 = line[1]
#         dist = int(line[2])
#         romania.setdefault(ct1, []).append(ctNode(ct2, dist))
#         romania.setdefault(ct2, []).append(ctNode(ct1, dist))


# def makehuristikdict():
#     h = {}
#     with open("romania_sld.txt", 'r') as file:
#         for line in file:
#             line = line.strip().split(",")
#             node = line[0].strip()
#             sld = int(line[1].strip())
#             h[node] = sld
#     return h


# def heuristic(node, values):
#     return values[node]

# def caculateProfitOfEachSaleman(sman, cluster, orderItem, deplot):
#     distance = totalDistanceForEachCluster(sman, cluster, deplot)
#     cost = caculateCostOfEachSalesman(distance)
#     salary = caculateSalaryOfEachSalesman(orderItem, sman, cluster)
#     profit = salary - cost
#     return profit
if __name__ == "__main__":
    assign2('input.txt', 'output.txt')