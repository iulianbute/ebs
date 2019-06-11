
class Ext:
    input             = '.zip'
    objectProjections = '.proj'
    environment       = '.env'
    processedData     = '.proc'
    widths            = '.widths'


environmentError = 0.05

def getEnvironment(scenes):
    # calculeaza 'mediul inconjurator' din scene
    scenesNo = len(scenes[0])
    alfaNo = len(scenes[0][0])
    envScene = []
    envDist = lambda scns,snsInd,dstInd: max([scns[scnInd][snsInd][dstInd] for scnInd in range(len(scns))])
    for sensId in range(scenesNo):
        envScene.append([envDist(scenes, sensId, alfa) for alfa in range(alfaNo)])
    return envScene

def getObjectDist(objDist, envDist):
    # verifica daca punctul este din 'mediul inconjurator' sau din obiect
    if envDist - objDist < environmentError * envDist:
        return 0
    return objDist

def getObject(scene, environment):
    objectData = []
    for sensInd in range(len(scene)):
        # izoleaza proiectia obiectului de 'mediul inconjurator'
        allSensorData = [getObjectDist(s, e) for s,e in zip(scene[sensInd], environment[sensInd])]
        selSensorData = []
        # se pastreaza numai date de interes
        for i in range(len(allSensorData)):
            if allSensorData[i-1]+allSensorData[i] > 0:
                selSensorData.append(allSensorData[i])
        # se roteste proiectia incat sa inceapa de la indexul 0
        if len(selSensorData) > 0:
            if selSensorData[0] != 0: 
                lastZero = len(selSensorData) - 1 - selSensorData[::-1].index(0)
                selSensorData = selSensorData[lastZero:] + selSensorData[:lastZero]
            selSensorData = selSensorData[1:-1]
        objectData.append(selSensorData)
    return objectData
