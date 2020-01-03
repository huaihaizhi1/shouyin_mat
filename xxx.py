import time
import dateutil.parser
import datetime
def date_s_date(m1,param,n):        ###前端修改时间#######param('Z','GMT')
    if param=='Z':
        if n=='day':
            d = dateutil.parser.parse(m1)
            current_time = (d + datetime.timedelta(hours=8)).strftime('%Y-%m-%d')
        else:
            d = dateutil.parser.parse(m1)
            current_time = (d + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
    elif param=='GMT':
        if n=='day':
            dd = m1
            GMT_FORMAT = '%a %b %d %Y %H:%M:%S GMT+0800'
            current_time=datetime.datetime.strptime(dd, GMT_FORMAT).strftime('%Y-%m-%d')
        else:
            dd = m1
            GMT_FORMAT = '%a %b %d %Y %H:%M:%S GMT+0800'
            current_time=datetime.datetime.strptime(dd, GMT_FORMAT)

    return current_time

print(date_s_date('2020-01-02T16:00:00.000Z','Z','day'))
print(date_s_date('Fri Jan 03 2020 23:59:59 GMT+0800','GMT','day'))