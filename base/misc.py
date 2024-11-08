def getDataFromDict(dictObj:dict,key:object):
    if(dictObj != None):
        if(key in dictObj):
            return dictObj[key]
    return None