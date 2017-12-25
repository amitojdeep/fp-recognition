import math
import menpo
import numpy as np
from menpo.shape import PointCloud
import csv
import copy

filesTest = [1,2,12,14,20,21]
filesAll = [1,2,12,14,20,21,22,26,27,31,35,37,43,54,55,56,61,67,72,76,89,92,94,95,98]
xyt_path = "xyt_rand/"
output = "newOp/"
err = []


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

def save_to_csv(template, train1, test1, test2):
    with open(output + "ver" + str(train1) + "_"  + str(test1) + "_" + str(test2) + ".csv", "wb") as f:
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

def matchStrict(p1, p2):
    dist = abs((int(round(p2[0] - p1[0]))) ** 2 + (int(round(p2[1] - p1[1]))) ** 2)**0.5
    theta = abs(min(p2[2] - p1[2], 360 - (p2[2] - p1[2])))
    if dist < 4 and theta < 7:
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

    """curr = 0
    for m1 in t1:
        for m2 in t2:
            match_list.append([m1,m2,num_matched[curr]])
            curr = curr + 1
    match_list.sort(key=takeThird)
    for row in match_list:
        print row"""

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

def prever(t1, t2):
    it = 15
    t2best = copy.deepcopy(t2) #the best transformation of t2 over all iterations
    prev = 0
    for ma in t1:
        for mb in t2:
            if match(ma, mb):
                prev = prev + 1
    print prev
    for x in range(it):
        mx, t2trns = geometricMatching(t1, t2)
        print "matched geometrically", mx
        if mx > prev:
            prev = mx
            t2best = copy.deepcopy(t2trns)
        t2 = copy.deepcopy(t2trns)
        if mx < 10:
            break

        """Menpo thin plate spline code"""
        if x == it-1:
            break
        src = []
        tar = []
        m2incl = [0 for z in range(len(t2))]  # checks if a point is already included
        for m1 in t1:
            probs = [] #probable matches for src pt, could be empty
            for m2 in t2: #try with each point in m2
                if matchStrict(m1, m2) == 1:
                    probs.append(m2)
                best = []
            if len(probs) == 0:
                continue # no matching target point, continue to nezt source minutiae

            for k in probs:
                if len(best) == 0:
                    best = copy.deepcopy(k)
                else:
                    dx1 , dy1, dt1 = compare(m1, best)
                    dx2, dy2, dt2 = compare(m1, k)
                    if abs(dt2) < abs(dt1):
                        best = copy.deepcopy(k)
            src.append([m1[0], m1[1]])
            tar.append([best[0], best[1]])

        if len(src) < 3:
            print "Too few control points"
            break
        tr = menpo.transform.ThinPlateSplines(PointCloud(np.array(src)), PointCloud(np.array(tar)),
                                              min_singular_val = 0.000001)
        npt2 = np.empty([len(t2), 2])
        for i, m2 in enumerate(t2):
            npt2[i] = [m2[0], m2[1]]
        res = tr.apply(npt2, batch_size=16)
        resarr = np.asarray(res)
        temp = []
        for i, ele in enumerate(resarr):
            temp.append([ele[0], ele[1], t2[i][2], t2[i][3]])
        t2 = copy.deepcopy(temp)

    return t2best


for test1 in filesTest:
    for test2 in range(5, 9):
        # t1 = readMinutiae(test1,test2)
        for train1 in filesAll:
            t1 = readMinutiae(test1, test2)
            for train2 in range(1, 5):
                print "testfile:", test1, test2
                print "verified against:", train1, train2

                t2 = readMinutiae(train1, train2)
                try:
                    t2trns = copy.deepcopy(prever(t1, t2))
                    merge(t1, t2trns)
                except:
                    print "Exception!"
                    try:
                        t1 = merge(t1, geometricMatching(t1, t2))
                    except:
                        print "Geometric Match also failed :("
                        err.append([test1, test2, train1, train2])
            save_to_csv(t1, train1, test1, test2)

work()
print err