import random
import fparser as P
import sys
import math
import os
from sklearn.cluster import DBSCAN
from threading import Thread
import time

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
  initial_load_file = time.time()
  fl = P.loadFile(which)
  final_load_file = time.time()
  load_file_time = final_load_file - initial_load_file
  means = []
  smeans = 0
  load_scenes_sum = 0
  for scene in range(50):
    initial_load_scene = time.time()
    pts = P.loadScene(fl, scene)
    final_load_scene = time.time()
    load_scenes_sum += final_load_scene - initial_load_scene
    if len(pts) == 0:
      break
    res, std, centroid = getMean(pts)
    pts = removeNoise(pts, res, std, centroid)
    res, _, _ = getMean(pts)
    smeans += res
    means.append(res)
  smeans /= 50
  print('Total reading time: {}'.format(load_file_time + load_scenes_sum))
  return smeans, 50 / (load_file_time + load_scenes_sum)

def trainAll():
  res = {}
  for d in os.listdir(sys.argv[1]):
    print('Training', d)
    s, time = trainOne(os.path.join(sys.argv[1], d, 'in.csv'))
    print("Reading tuples / second: {}".format(time))
    print('Done with result', s)
    res[d] = s
  open(sys.argv[2], 'w').write('{0}'.format(res))

def closestObject(m, data):
    best = (500000000.0, '')
    for key in data:
        if abs(m - data[key]) < best[0]:
            best = (abs(m - data[key]), key)
    return best[1]


def processScene(fl, data, scene, reses, global_latency, load_time):
  load_scene_time = time.time() 
  pts = P.loadScene(fl, scene)
  load_scene_time = time.time() - load_scene_time
  if len(pts) == 0:
    return
  clusters = clusterize(pts)
  #print('For scene {0} I have {1} clusters'.format(scene, len(clusters)))
  initial_time = time.time()
  res = {}
  for cluster in clusters:
    #print(cluster)
    m = getMean(cluster)[0]
    obj = closestObject(m, data)
    if obj not in res:
      res[obj] = 0
    res[obj] += 1
  reses[scene] = res
  latency = time.time() - initial_time
  global_latency[scene] = latency
  load_time[scene] = load_scene_time

def runInstance(which, data):
  time_loading_data_file = time.time()
  fl = P.loadFile(which)
  time_loading_data_file = time.time() - time_loading_data_file
  nr = 100
  L = [None] * nr
  threads = []
  global_latency = [0] * nr
  load_scene_time = [0] * nr
  initial_time = time.time()
  for scene in range(nr):
    process = Thread(target=processScene, args=[fl, data, scene, L, global_latency, load_scene_time])
    threads.append(process)
    process.start()
    #res = processScene(fl, data, scene, L)
    #break
  for process in threads:
    process.join()
  finish_time = time.time()
  #total_loading_data_time = time_loading_data_file + sum(load_scene_time)
  total_loading_data_time = sum(load_scene_time)
  print(load_scene_time)
  return L, round(sum(global_latency) / nr, 2), round(nr / sum(global_latency), 2), round(nr / total_loading_data_time, 2)


def formatOutput(res):
    s = []
    for key in res:
        s.append(key)
        s.append('{0}'.format(res[key]))
    return ','.join(s)


def main(result_file_name="result"):
  data = eval(open(sys.argv[1]).read())
  L, latency, throughput, loading_time = runInstance(sys.argv[2], data)
  result_file = open(result_file_name, "w")
  for i in range(len(L)):
    if L[i] is None:
      continue
    s = '{0},{1}'.format(i, formatOutput(L[i]))
    result_file.write(s)
    result_file.write('\n')
  print("Reading tuples / second: {} | Solution latency: {} | Solution throughput: {}".format(loading_time, latency, throughput))
  result_file.close()

if __name__ == '__main__':
  if len(sys.argv) > 3 and sys.argv[3] == '--train':
    trainAll()
  else:
    main()
  #trainAll()
