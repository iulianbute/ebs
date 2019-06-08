from sys import argv
from dataReader import readData, getFiles, loadOrCompute, compute
from dataProcessor import getEnvironment, getObject, Ext

trainDir = 'train'

def learnObject(zipFileName):
    fileName = zipFileName[:-4]
    print fileName
    scenes      = lambda: loadOrCompute(fileName+Ext.processedData, lambda: readData(zipFileName))
    scenesEnv   = lambda: loadOrCompute(fileName+Ext.environment, lambda: getEnvironment(scenes()))
    getObj      = lambda s: getObject(s, scenesEnv())
    return loadOrCompute(fileName+Ext.objectProjections, lambda: map(getObj, scenes()))
    
    
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
    objectsProjs = map(learnObject, toLearn)
    cStats = map(stats, objectsProjs)
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
