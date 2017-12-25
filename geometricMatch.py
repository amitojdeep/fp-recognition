import math
import csv

output = "plots/"
xyt_path = "database/"

def takeThird(elem):
    return elem[2]

def readMinutiae(x1, y1):
    """reads x_y.jpg.xyt
    returns list of 5 element lists (x,y,theta, quality, matches = 1)"""
    with open(xyt_path + str(x1) + "_" + str(y1) + ".jpg.xyt") as fp1:
        fl = fp1.readlines()
        f = []
        for l in fl:
            l1 = l.split()
            l2 = []
            for num in l1:
                l2.append(int(num))
            l2.append(1) # number of times a minutiae is found
            f.append(l2)
    return f

def save_to_csv(template, train1, train2, test1, test2):
    with open(output + "ver" + str(train1) + "_" + str(train2) + "_" + str(test1) + "_" + str(test2) + ".csv", "wb") as f:
        writer = csv.writer(f, delimiter =' ')
        writer.writerows(template)

def compare(p1, p2): #used to get difference in x & y distance and theta of minutiae pairs p1 & p2
    dX = p1[0] - p2[0]
    dY = p1[1] - p2[1]
    dTheta =(p1[2] - p2[2])
    return dX, dY, dTheta

def transform(t2, dx, dy, dtheta, mref): #rigidly transforms every minutiae point in t2
    t2New = []
    for m2 in t2:
        a = round((m2[0] - mref[0])*math.cos(dtheta) - (m2[1] - mref[1])*math.sin(dtheta) + dx + mref[0])
        b = round((m2[0] - mref[0])*math.sin(dtheta) + (m2[1] - mref[1])*math.cos(dtheta) + dy + mref[1])
        theta = m2[2] + dtheta
        q = m2[3]
        t2New.append([a, b, theta, q])
    return t2New

def match(p1, p2):
    dist = abs((int(round(p2[0] - p1[0]))) ** 2 + (int(round(p2[1] - p1[1]))) ** 2)**0.5
    theta = abs(min(p2[2] - p1[2], 360 - (p2[2] - p1[2])))
    if dist < 8 and theta < 12:
        return 1
    return 0

def merge(ta, tb):
    cnt  = 0
    for i, ma in enumerate(ta):
        for mb in tb:
            """if math.isinf(ma[0]) or math.isinf(ma[1]) or math.isinf(mb[0]) or math.isinf(mb[1]) or math.isnan(
                    ma[0]) or math.isnan(ma[1]) or math.isnan(mb[0]) or math.isnan(mb[1]):
                continue"""
            if match(ma, mb):
                ta[i][4] = ma[4] + 1
                cnt = cnt + 1
    print "matched in merge", cnt
    return ta

def geometricMatching(t1, t2): #matches using theta and distance
    t2arr = []  # array of transformed template
    for m1 in t1:
        for m2 in t2:
            dx, dy, dtheta = compare(m1, m2) #relative coordinates a
            t2new = transform(t2, dx, dy, dtheta, m2)#m2 goes as reference minutiae
            t2arr.append(t2new)

    num_matched = [0 for y in range(len(t2arr))]  # counts number of matched minutiae
    match_list = []
    # for each transformed template wrt original template
    for index, t2it in enumerate(t2arr):  # checking for maximum matching points per template
        for m1 in t1:
            for m2 in t2it:
                if match(m1, m2) == 1:
                    num_matched[index] = num_matched[index] + 1

    curr = 0
    for m1 in t1:
        for m2 in t2:
            match_list.append([m1,m2,num_matched[curr]])
            curr = curr + 1
    match_list.sort(key=takeThird)
    for row in match_list:
        print row

    mx = -1
    mx_pos = -1
    for i, val in enumerate(num_matched):
        if val > mx:
            mx = val
            mx_pos = i
    if mx_pos == -1 or mx < 4:
        print "Not transformed"
        return mx, t2  # no transform
    return mx, t2arr[mx_pos]



t1 = readMinutiae(1,5)
t2 = readMinutiae(1,4)
for i in  range(20):
    mx, t2 = geometricMatching(t1, t2)
merge(t1, t2)
save_to_csv(t1,1,4,1,5)
