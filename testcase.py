import numpy as np

# Hàm tạo testcase
def genTest(filename):
    # Số đơn hàng
    numOfOrders = np.random.randint(1,20)
    # Số nhân viên giao hàng
    numOfSalesman = np.random.randint(1,numOfOrders)
    # Tọa độ đơn hàng nhỏ nhất và lớn nhất
    maxX = 10
    maxY = 10
    # Tọa độ kho
    x=np.random.randint(1,maxX)
    y=np.random.randint(1,maxY)

    # Ghi testcase ra file
    fo = open(filename, "w")
    fo.write(str(x) + " " + str(y) + "\n")
    fo.write(str(numOfSalesman) + " " + str(numOfOrders) + "\n")

    for i in range(numOfOrders):
        x=np.random.randint(1,maxX)
        y=np.random.randint(1,maxY)
        v=np.random.randint(1,5)
        m=np.random.randint(1,5)
        fo.write(str(x) + " " + str(y) + " " + str(v) + " " + str(m))
        if i != (numOfOrders - 1):
            fo.write('\n')

def caculateSolution(filename):
    pass

if __name__=='__main__':
    genTest("input.txt")