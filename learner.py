from sys import argv
from dataReader import readData, getFiles, loadOrCompute, compute
from dataProcessor import getEnvironment, getObject, Ext
from math import cos, sqrt
from multiprocessing import Pool

trainDir = 'train'

def computeWidths(projection):
    new_sensor_data = []
    for sensor_data in projection:
        if len(sensor_data) == 0:
            new_sensor_data.append(0)
            continue
        angle = 360.0 * len(sensor_data) / 1125.0
        cos_c = cos(angle)
        a = sensor_data[0]
        b = sensor_data[-1]
        value = a * a + b * b - 2 * cos_c * a * b
        new_sensor_data.append(round(sqrt(value), 2))
    # old_sum = sum(new_sensor_data)
    # if old_sum != 0:
    #     new_sensor_data = [round(x / old_sum, 3) for x in new_sensor_data]
    return tuple(new_sensor_data)


def learnObject(zipFileName):
    fileName = zipFileName[:-4]
    print fileName
    scenes      = lambda: loadOrCompute(fileName+Ext.processedData, lambda: readData(zipFileName))
    scenesEnv   = lambda: loadOrCompute(fileName+Ext.environment, lambda: getEnvironment(scenes()))
    getObj      = lambda s: getObject(s, scenesEnv())
    projections = lambda: loadOrCompute(fileName+Ext.objectProjections, lambda: map(getObj, scenes()))
    objWidths   = lambda: loadOrCompute(fileName+Ext.widths, lambda: map(computeWidths, projections()))
    return objWidths()

def stats(objectProjs):
    sensLim = []
    for sensId in range(64):
        sensMax = 0
        sensMaxLen = 0
        for scene in objectProjs:
            sensMax = max([sensMax] + scene[sensId])
            sensMaxLen = max(sensMaxLen, len(scene[sensId]))
        sensLim.append((round(sensMax,2), sensMaxLen))
    return sensLim
    

def learn(toLearn):
    if type(toLearn) == str: toLearn = getFiles(toLearn, Ext.input)
    customPool = Pool(processes=2)
    #result = map(learnObject, toLearn)
    result = customPool.map(learnObject, toLearn)
    return result
    cStats = map(stats, result)
    cStats1 = [[ss[1] for ss in s] for s in cStats]
    ss = []
    for i in range(64):
        ss.append(max([s[i] for s in cStats1]))
    with open('stats.out', 'w') as out:
        out.write('\n'.join(['%-35s %s'%(o, str(s)) for s, o in zip(cStats, toLearn)]))
        out.write('\n\n')
        out.write('\n'.join(['%-35s %s'%(o, str(s)) for s, o in zip(cStats1, toLearn)]))
        out.write('\n\n' + str(ss))
        out.write('\n\n' + str(max(ss)))
    

if __name__=='__main__':
    if len(argv) > 1: learn(argv[1:])
    else: learn(trainDir)
