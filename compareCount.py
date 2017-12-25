import csv
output = "newOp/"
filesAll = [1,2,12,14,20,21,22,26,27,31,35,37,43,54,55,56,61,67,72,76,89,92,94,95,98]

def readMinutiae(i, j, k):
    """reads x_y.csv
    returns list of 5 element lists (x,y,theta, quality, matches)"""
    with open(output + "ver" + str(i) + "_" + str(j) + "_" + str(k) + ".csv") as fp1:
        fl = fp1.readlines()
        f = []
        for l in fl:
            l1 = l.split()
            l2 = []
            for num in l1:
                l2.append(int(num))
            f.append(l2)
    return f

def save_to_res(tmp):
    with open("cmp2.txt","wb") as f:
        writer = csv.writer(f, delimiter =' ')
        writer.writerows(tmp)

def counter(minLevel, x, y,w):
    #print 'fp', x
    cnt = 0
    tinit = readMinutiae(x, y,w)

    for m in tinit:
        if m[4] >= minLevel:
            cnt = cnt + 1
            #tfinal.append([m[0], m[1], m[2], m[3]])
    return cnt


c = 0
cntArr = []
for x in filesAll: #train
    for y in filesAll: #test prefix part
        for w in range(5,9): #test suffix part
            cntArr.append([x, y, w, counter(2, x, y, w)])
            c = c + 1
print c
save_to_res(cntArr)

