import random
import fparser as P
import sys
import math
import os
from sklearn.cluster import DBSCAN
from threading import Thread

def rpt():
    return random.random() * 100 - 200

def euclid(A, B):
    [a, b, c] = A
    [x, y, z] = B
    da = a - x
    db = b - y
    dz = c - z
    return math.sqrt(da * da + db * db + dz * dz)

def clusterize(pts):
    clustering = DBSCAN(eps=7.5, min_samples=10).fit(pts)
    labels = clustering.labels_
    res = {}
    for idx in range(len(pts)):
        lbl = labels[idx]
        if lbl < 0:
            continue
        if lbl not in res:
            res[lbl] = []
        res[lbl].append(pts[idx])
    resl = []
    for key in res:
        resl.append(res[key])
    return resl

def getMean(pts):
    centroid = [0, 0, 0]
    for pt in pts:
        for dim in range(3):
            centroid[dim] += pt[dim]
    for dim in range(3):
        if len(pts) != 0:
            centroid[dim] /= len(pts)
    dst = 0
    for pt in pts:
        e = euclid(pt, centroid)
        dst += e * e
    if len(pts) != 0:
        dst /= len(pts)
    return dst, math.sqrt(dst), centroid


def removeNoise(pts, var, std, centroid):
	# Noise and outlier removal
	new_pts = []
	for pt in pts:
		dst = euclid(pt, centroid)
		if dst <= std * 2:
			new_pts.append(pt)
	return new_pts


def trainOne(which):
    fl = P.loadFile(which)
    means = []
    smeans = 0
    for scene in range(50):
        pts = P.loadScene(fl, scene)
        res, std, centroid = getMean(pts)
        pts = removeNoise(pts, res, std, centroid)
        res, _, _ = getMean(pts)
        smeans += res
        means.append(res)
    smeans /= 50
    return smeans

def trainAll():
    res = {}
    for d in os.listdir(sys.argv[1]):
        print('Training', d)
        s = trainOne(os.path.join(sys.argv[1], d, 'in.csv'))
        print('Done with result', s)
        res[d] = s
    open(sys.argv[2], 'w').write('{0}'.format(res))

def closestObject(m, data):
    best = (500000000.0, '')
    for key in data:
        if abs(m - data[key]) < best[0]:
            best = (abs(m - data[key]), key)
    return best[1]

def processScene(fl, data, scene, reses):
    pts = P.loadScene(fl, scene)
    clusters = clusterize(pts)
    #print('For scene {0} I have {1} clusters'.format(scene, len(clusters)))
    res = {}
    for cluster in clusters:
        #print(cluster)
        m = getMean(cluster)
        obj = closestObject(m, data)
        if obj not in res:
            res[obj] = 0
        res[obj] += 1
    reses[scene] = res

def runInstance(which, data):
    fl = P.loadFile(which)
    nr = 100
    L = [None] * nr
    threads = []
    for scene in range(nr):
        process = Thread(target=processScene, args=[fl, data, scene, L])
        threads.append(process)
        process.start()
        #res = processScene(fl, data, scene, L)
        #break
    for process in threads:
        process.join()
    return L

def formatOutput(res):
    s = []
    for key in res:
        s.append(key)
        s.append('{0}'.format(res[key]))
    return ','.join(s)

def main():
    data = eval(open(sys.argv[1]).read())
    L = runInstance(sys.argv[2], data)
    for i in range(len(L)):
        s = '{0},{1}'.format(i, formatOutput(L[i]))
        print(s)

if __name__ == '__main__':
    main()
