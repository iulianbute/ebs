from zipfile import ZipFile
from numpy import sqrt, arctan2, pi
import os
from pickle import dump, load


getFiles = lambda dir, ext='': [os.path.join(dir, f) for f in os.listdir(dir) if f.endswith(ext)]

def compute(f, funct):
    result = funct()
    dump(result, open(f, 'wb'), protocol = -1)
    return result


def loadOrCompute(f, funct):
    if os.path.isfile(f): 
        return load(open(f, 'rb'))
    return compute(f, funct)
    

polCoord = lambda x,y: ((arctan2(y, x)/pi*180 + 360)%360, sqrt(x**2 + y**2))
def getLineData(line): 
    #sceneId, sensorId, coordonate polare
    #fiind numar fix de puncte/rotatie, unghiul se poate elimina daca distantele sunt sortate
    sceneTime,sensorId,x,y,z = map(float, line.strip().split(','))
    return [int(sceneTime+0.1), sensorId, polCoord(x,z)]

def normalizeSensorData(sensorData):
    #sorteaza dupa unghi si il elimina 
    return map(lambda p: p[1], sorted(sensorData, key = lambda p: p[0]))

def normalizeScenes(scenes):
    normalizeScene = lambda sensorsData: map(normalizeSensorData, [sensorsData[sensorId] for sensorId in sorted(sensorsData.keys())])
    return map(normalizeScene, [scenes[sceneId] for sceneId in sorted(scenes.keys())])

def readData(fileName):
    # face dictionar sceneId:sensorId:[distances]
    print 'Reading..',
    linesData = filter(lambda l: len(l)>9, ZipFile(fileName).open('in.csv').readlines())
    print 'Preprocessing..',
    linesData = map(getLineData, linesData)
    scenes = dict()
    for scene, sensor, coord in filter(lambda l: l[2] != (0, 0), linesData): 
        scenes.setdefault(scene, dict()).setdefault(sensor, list()).append(coord)
    print 'Normalization..',
    scenes = normalizeScenes(scenes)
    print 'Done.'
    return scenes    
    
