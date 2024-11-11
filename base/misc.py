import re
from datetime import datetime

def get_data_from_dict(dictObj:dict,key:object):
    if(dictObj != None):
        if(key in dictObj):
            return dictObj[key]
    return None

def average(range:list):
    return sum(range)/len(range)

def get_date(text:str):
    print(text)
    #2024-10-11 00:00:00+05:30
    match = re.search(r'\d{4}-\d{2}-\d{2}', text)
    if(match != None):
        date = datetime.strptime(match.group(), '%Y-%d-%m').date()
        return date.strftime('%d-%m-%Y')
    return text

def get_change(initial:float,final:float)->float:
    return (final - initial) / initial

def get_change_percentage(initial:float,final:float,n_digits:int=2)->float:
    return round((final - initial) / initial * 100,2)

def get_round(data):
    return round(data,3)

def get_format(data):
    return "{:,}".format(data)