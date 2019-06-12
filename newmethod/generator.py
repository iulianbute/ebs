import os
import sys
import random
import fparser as P
import solution as S

perSensor = 1100

def getOneObject(examples, keepAll):
  L = os.listdir(examples)
  idx = random.randint(0, len(L) - 1)
  which = L[idx]
  fl = P.loadFile(os.path.join(examples, which, 'in.csv'))
  scene = random.randint(0, 49)
  pts = P.loadScene(fl, scene, keepAll, True)
  #if keepAll:
  #  print('Expected {0} points per sensor'.format(len(pts[0])))
  return (pts, which)

def slopeOf(A):
  [x, y, z] = A
  if x == 0:
    x += 0.00001
  return z / x

def elimOne(L):
  minDelta = None
  for idx in range(len(L) - 1):
    (slope0, _) = L[idx]
    (slope1, _) = L[idx + 1]
    deltaSlope = abs(slope1 - slope0)
    if (minDelta is None) or deltaSlope < minDelta[0]:
      minDelta = (deltaSlope, (idx, idx + 1))
  (_, (x, y)) = minDelta
  dstX = S.euclid(L[x][1], [0, 0, 0])
  dstY = S.euclid(L[y][1], [0, 0, 0])
  which = x if dstX > dstY else y
  L = L[:x] + L[(x + 1):]
  return L

def adjustSomePts(pts):
  L = []
  for pt in pts:
    L.append((slopeOf(pt), pt))
  L = sorted(L)
  while len(L) > perSensor:
    L = elimOne(L)
  pts = []
  for elem in L:
    pts.append(elem[1])
  return pts

def adjustAllPts(pts):
  for key in pts:
    #print('Now adjusting points for sensor {0} ({1})'.format(key, len(pts[key])))
    pts[key] = adjustSomePts(pts[key])
  return pts

def genScene(examples, nrObj):
  allObj = {}
  pts = {}
  flag = True
  for _ in range(nrObj):
    (opts, owhich) = getOneObject(examples, flag)
    flag = False
    for key in opts:
      if key not in pts:
        pts[key] = []
      pts[key].extend(opts[key])
    if not owhich in allObj:
      allObj[owhich] = 0
    allObj[owhich] += 1
  pts = adjustAllPts(pts)
  return (pts, allObj)

def ptsToInputFormat(pts):
  periodSize = 72000
  offsetSize = 1600
  lines = []
  while len(lines) < offsetSize:
    lines.append('0.0,0,0.0,0.0,0.0')
  for key in pts:
    for pt in pts[key]:
      lines.append('0.001922,{0},{1},{2},{3}'.format(key, pt[0], pt[1], pt[2]))
  while len(lines) < periodSize:
    lines.append('0.0,0,0.0,0.0,0.0')
  return '\n'.join(lines)

def main():
  (pts, allObj) = genScene(sys.argv[1], 20)
  if not os.path.isdir(sys.argv[2]):
    os.makedirs(sys.argv[2])
  open(os.path.join(sys.argv[2], 'in.csv'), 'w').write(ptsToInputFormat(pts))
  open(os.path.join(sys.argv[2], 'out.csv'), 'w').write(S.formatOutput(allObj))

  #for key in pts:
  #  print('Got {0} points in sensor {1}'.format(len(pts[key]), key))

if __name__ == '__main__':
  main()
