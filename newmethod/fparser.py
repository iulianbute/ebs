import sys
import math

def loadFile(incsv):
  return open(incsv).readlines()

def loadScene(lines, which, keepEnv = False, bySensor = False):
  periodSize = 72000
  offsetSize = 1600
  startPos = which * periodSize
  endPos = startPos + periodSize
  startPos += offsetSize
  data = [0] * 64
  for ln in lines[startPos:endPos]:
    ln = ln.split(',')
    sensor = int(ln[1])
    x = float(ln[2])
    y = float(ln[3])
    z = float(ln[4])
    dst = math.sqrt(x*x + y*y + z*z)
    data[sensor] = max([data[sensor], dst])
  if bySensor:
    pts = {}
  else:
    pts = []
  for ln in lines[startPos:endPos]:
    ln = ln.split(',')
    sensor = int(ln[1])
    x = float(ln[2])
    y = float(ln[3])
    z = float(ln[4])
    dst = math.sqrt(x*x + y*y + z*z)
    if not keepEnv:
      if abs(dst - data[sensor]) < 0.1:
        continue
    if bySensor:
      if sensor not in pts:
        pts[sensor] = []
      pts[sensor].append([x, y, z])
    else:
      pts.append([x, y, z])
  #lines = list(map(lambda x : list(map(float, x.strip().split(',')[-3:])), ))
  return pts

def main():
  pts = loadScene(loadFile(sys.argv[1]), 0)
  for pt in pts:
    print(','.join(list(map(str, pt))))

if __name__ == '__main__':
  main()
