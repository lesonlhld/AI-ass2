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
    for x in orderItem:
        v, m = orderItem[x]
        orderItem[x] = 5 + v + m * 2
    return orderItem

def caculateCostOfEachSalesman(distance):
    return distance / 40 *20 + 10

def caculateSalaryOfEachSalesman(orderItem, sman, cluster):
    salary = 0
    for i in range(len(cluster[sman])):
        salary += orderItem[tuple(cluster[sman][i])]
    return salary

def distanceBetweenTwoPoints(P1, P2):
    return np.sqrt((P1[0]-P2[0])**2+(P1[1]-P2[1])**2)

def totalDistanceForEachCluster(sman, cluster, deplot):
    dist = 0
    clusterdist = [deplot]
    clusterdist += [cluster[sman][i] for i in range(len(cluster[sman]))]
    clusterdist = np.array(clusterdist)
    
    for i in range(len(cluster[sman])):
        dist+=distanceBetweenTwoPoints(clusterdist[i],clusterdist[i+1])
    return dist

    
def Ploteachcluster(cluster, distance, deplot):
    colours = ['c','crimson','green','black','blue']
    k=0
    
    # p1 = pl.Rectangle((0,0),0.1,0.1,fc=colours[0])
    # p2 = pl.Rectangle((0,0),0.1,0.1,fc=colours[1])
    # p3 = pl.Rectangle((0,0),0.1,0.1,fc=colours[2])
    # p4 = pl.Rectangle((0,0),0.1,0.1,fc=colours[3])
    # p5 = pl.Rectangle((0,0),0.1,0.1,fc=colours[4])
    # pl.legend((p1,p2,p3,p4,p5),('Salesman1','Salesman2','Salesman3','Salesman4','Salesman5'),loc='center right')
    
    
    pl.title('Total distance=' + str(distance))
    pl.xlim(xmin=0,xmax=maxX + 5)
    pl.ylim(ymin=0,ymax=maxY + 5)

    for sman in cluster:
        Pt = [deplot]
        # Pt = [sman]
        Pt += [cluster[sman][i] for i in range(len(cluster[sman]))]
        Pt = np.array(Pt)
        
        pl.plot(Pt[:,0],Pt[:,1],marker='o',c=colours[k])
        k+=1

    pl.show()
    

def kmeans(deplot, orders):
    S = randomPositionOfSalesman(numOfSalesman)
    S = np.array(S)

    cluster = {}
   
    for x in range(0,len(S)):
         key = tuple(S[x])
         cluster[key] = []
         
         
    for i in range(len(numOfOrders)):
        min = 99999999
        min_s = []
        min_r = []
        for j in range(len(S)):
            if(min > distanceBetweenTwoPoints(orders[numOfOrders[i]],S[j])):
                min = distanceBetweenTwoPoints(orders[numOfOrders[i]],S[j])
                min_s = S[j]
                min_r = orders[numOfOrders[i]]
        
        tmp_arr = cluster[tuple(min_s)]
        tmp_arr.append(min_r)
        cluster[tuple(min_s)] = tmp_arr

    if (len(cluster) != numOfSalesman) or ([] in cluster.values()):
        kmeans(deplot, orders)
    else:
        distance = {}
        cost = {}
        salary = {}
        for sman in cluster:
            distance[sman] = totalDistanceForEachCluster(sman, cluster, deplot)
            cost[sman] = caculateCostOfEachSalesman(distance[sman])
            salary[sman] = caculateSalaryOfEachSalesman(orderItem, sman, cluster)
        
        check = False
        for sman in cluster:
            if salary[sman] < cost[sman]:
                check = True
                kmeans(deplot, orders)
                break
        
        if check == False:
            salesman = list(cluster.keys())
            profit = [salary[x] - cost[x] for x in salesman]
            print(profit)
            while abs(profit[0] - profit[1]) > 3.5 or abs(profit[0] - profit[2]) > 3.5 or abs(profit[2] - profit[1]) > 3.5:
                check = True
                kmeans(deplot, orders)
                break

        for sman in cluster:
            if check == False:
                print(str(sman) + ": " + str(cluster[sman]))
                # print("Doanh thu: " + str(salary[sman]))
                # print("Quang duong: " + str(distance[sman]))
                # print("Chi phi: " + str(cost[sman]))
                print("Loi nhuan: " + str(salary[sman] - cost[sman]))
        if check == False:
            distance=np.array(list(distance.values()))
            Ploteachcluster(cluster, distance, deplot)
        #SA_new(cluster)
    
def swap(cluster, nsman):
    x = len(cluster[nsman])
    r1 = np.random.randint(0,x)
    r2 = np.random.randint(0,x)
    r3 = np.random.randint(0,x)
    r4 = np.random.randint(0,x)

    temp = cluster[nsman][r1]
    cluster[nsman][r1] = cluster[nsman][r2]
    cluster[nsman][r2] = temp
    temp = cluster[nsman][r3]
    cluster[nsman][r3] = cluster[nsman][r4]
    cluster[nsman][r4] = temp
   
    return cluster[nsman]
     

def SA_new(cluster):
    S = randomPositionOfSalesman(numOfSalesman)
    S = np.array(S)

    new_cluster = {}
    solution = {}
    
    for x in range(0,len(S)):
        key1 = tuple(S[x])
        solution[key1] = []    
    
    
    for x in range(0,len(S)):
         key = tuple(S[x])
         new_cluster[key] = []    
    
    count=0
    
    temperature = 1e+10
    cooling_rate = 0.95
    temperature_end = 0.000000001
    
    while temperature > temperature_end:   
        count +=1
        
        #print (count)   
        for nsman in cluster:
            new_cluster[nsman] = []
                    
            dist = totalDistanceForEachCluster(nsman,cluster)  
           
            
            next_order = swap(cluster,nsman)
            """next_order = np.random.permutation(cluster[nsman])"""
            
            
            new_cluster[nsman] = next_order
           
            dist_new = totalDistanceForEachCluster(nsman,new_cluster)
            #print ("total distance is " + str(dist_new), nsman)
            
            difference = dist_new - dist
            
            
            if difference < 0 or math.e**(-difference/temperature) > np.random.rand():
                   
                solution[nsman] = new_cluster[nsman]
                
                """print( "solution is " + str(solution))"""
                final_dist = dist_new   
                print ("final total distance is " + str(final_dist), nsman)
                """Ploteachcluster(solution,final_dist)"""
                
            temperature = temperature * cooling_rate
        
        """Ploteachcluster(solution,final_dist)"""
        #Ploteachcluster(new_cluster,dist_new)


if __name__=='__main__':
    numOfOrders = range(5)
    numOfSalesman = 3
    maxX = 10
    maxY = 10
    # Deplot
    deplot = tuple([5, 5])
    
    orderItem = {}
    orders = []
    for i in range(len(numOfOrders)):
        x=np.random.randint(1,maxX)
        y=np.random.randint(1,maxY)
        v=np.random.randint(1,5)
        m=np.random.randint(1,5)
        orderItem[tuple([x, y])] = [v, m]
        orders.append([x, y])
    
    print("Orders are " + str(orders))
    print("Details are " + str(list(orderItem.values())))

    orderItem = caculateEarningsEachOrderItem(orderItem)
    orders = np.array(orders)

    kmeans(deplot, orders)