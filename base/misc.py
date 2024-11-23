import re
from datetime import datetime
from functools import wraps
import time
from logging import getLogger
import csv

logger = getLogger('uvicorn.error')

def get_data_from_dict(dictObj:dict,key:object):
    if(dictObj != None):
        if(key in dictObj):
            return dictObj[key]
    return None

def average(range:list):
    return sum(range)/len(range)
   
def get_float(data):
    try:
        if(isinstance(data, (int, float))):
            return data
        return float(data.strip())
    except:
        return 0

def get_date(text:str):
    #2024-10-11 00:00:00+05:30
    match = re.search(r'\d{4}-\d{2}-\d{2}', text)
    if(match != None):
        date = datetime.strptime(match.group(), '%Y-%d-%m').date()
        return date.strftime('%d-%m-%Y')
    return text

def get_datetime(text:str):
    if(text!=None and text!=''):
        return datetime.strptime(text,'%d-%m-%Y')
    return datetime.now()

def get_change(initial:float,final:float)->float:
    if(initial!=None and final != None and initial!=0):
        return (final - initial) / initial
    return 0

def get_change_percentage(initial:float,final:float,n_digits:int=2)->float:
    if(initial!=None and final != None and initial!=0):
        return round((final - initial) / initial * 100,2)
    return 0

def get_round(data):
    if(data!=None):
        return round(data,3)
    return 0

def get_format(data):
    if(data!=None):
        return "{:,}".format(data)
    return 0

def get_percentage_format(data:float):
    if(data is not None):
        return '{:.2%}'.format(get_float(data))
    return ''

def dt_from_epoch_ns(data:float)->datetime:
    try:
        return datetime.fromtimestamp(data/1000000000)
    except:
        return datetime.now()

def first_chars(data:str,separator:str='_',glue:str='')->str:
    return glue.join( [x[0] for x in data.split(separator)] )
    
def first_chars_list(data:str,separator:str=';',glue:str=',')->str:
    return glue.join([first_chars(x) for x in data.split(separator)])

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        
        logger.info(f'Function {func.__name__}{args} {kwargs} took {total_time:.4f} seconds.')
        
        return result
    return timeit_wrapper

def timeit_concise(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        
        logger.info(f'Function {func.__name__} took {total_time:.4f} seconds.')
        
        return result
    return timeit_wrapper

def timeit_concise_print(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        
        print(f'Function {func.__name__} took {total_time:.4f} seconds.')
        
        return result
    return timeit_wrapper

def read_csv(file_loc):
    with open(file_loc, mode ='r') as file:    
       csv_file = csv.DictReader(file)
       data = [row for row in csv_file]
       return data

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time
    
def market_open_india():
    start_now=datetime.datetime.now().replace(hour=9, minute=15, second=0, microsecond=0)
    end_now=datetime.datetime.now().replace(hour=15, minute=30, second=0, microsecond=0)
    return start_now<datetime.datetime.now()<end_now
    
clean_list = lambda list_obj : [x for x in list_obj if x is not None]
   


    