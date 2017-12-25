import csv
def readBozorthOut(filename = "newOp1.txt"):
    with open(filename) as f:
        scoreStrings = f.readlines()
        scores = []
        for s in scoreStrings:
            scores.append(float(s))
    return scores

def normalizeScores(scoreList):

    """for sc in scoreList:
        if sc > mx:
            mx  = sc
    print mx"""
    normScores = []
    for sc in scoreList:
        if sc > 700:
            n = 700
        else:
            n = (710 -sc)/(720)
        normScores.append(n)
    return normScores

def save_to_csv(output):
    with open("newOpProc1.txt", "wb") as f:
        writer = csv.writer(f, delimiter =' ')
        writer.writerows(output)

normalizedScores =  normalizeScores(readBozorthOut())
print len(normalizedScores)

files = [1,2,12,14,20,21,22,26,27,31,35,37,43,54,55,56,61,67,72,76,89,92,94,95,98]

cnt = 0 #count of element from normalizedScores to be selected

output = []

for i1 in files:
    for j1 in range(5,9):
        for i2 in files:
            for j2 in range(1,5):
                output.append([i1, j1, i2, j2, int(i1 == i2), normalizedScores[cnt]])
                cnt = cnt + 1

save_to_csv(output)


