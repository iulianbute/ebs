from os import chdir
from dataProcessor import getObject, getEnvironment, Ext
from dataReader import readData, getFiles, loadOrCompute


modelsDir = 'train'
testDir = 'test'

print 'Loading models projections..',
models = {f[len(modelsDir)+1:-len(Ext.objectProjections)]:loadOrCompute(f, lambda:0) for f in getFiles(modelsDir, Ext.objectProjections)}
for testFile in getFiles(testDir, Ext.input):
    testFile = testFile[:-len(Ext.input)]
    print testFile
    scenes  = lambda: loadOrCompute(testFile+Ext.processedData, lambda: readData(testFile))
    env     = lambda: loadOrCompute(testFile+Ext.environment, lambda: getEnvironment(scenes()))
    getObj  = lambda scn: getObject(scn, env())
    objectProjs = loadOrCompute(testFile+Ext.objectProjections, lambda: map(getObj, scenes()))
    print 'Stats:'
    sensLim = []
    for sensId in range(64):
        sensMin = 1000
        sensMax = 0
        for scene in scenes():
            sensMin = min([sensMin] + scene[sensId])
            sensMax = max([sensMax] + scene[sensId])
        sensLim.append((round(sensMin,2), round(sensMax,2)))
    print sensLim

