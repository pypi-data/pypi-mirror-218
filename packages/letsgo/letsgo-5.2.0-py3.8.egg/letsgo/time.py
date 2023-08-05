
from datetime import datetime

def current_date(f="%Y-%m-%d %H:%M:%S"):
    '''format date'''
    current_time = datetime.now()
    formatted = current_time.strftime(f)
    return formatted