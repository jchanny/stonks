'''
Utilities for calculating various options things
-------------------------------------------------
REVISION HISTORY:
  06/20 - Created
-------------------------------------------------'''

import datetime
from datetime import date

'''
returns the 3rd Friday of the month as YYYY-MM-DD
'''
def get3rdFriday(year,month):
    halfMonth = datetime.date(year, month, 15)
    halfMonthDay = halfMonth.weekday()
    if halfMonthDay != 4:
        return halfMonth.replace(day=(15 + (4 - halfMonthDay) % 7))
    return halfMonth #3rd friday is midway of month

def get3rdFridayNextMonth():
    today = date.today().strftime('%Y-%m-%d')
    split = today.split('-')
    year = int(split[0])
    month = (int(split[1]) + 1) % 12
    return get3rdFriday(year,month)




    
