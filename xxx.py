import dateutil.parser

def date_s_date(m1):
    d = dateutil.parser.parse(m1)
    return d.strftime('%Y-%m-%d %H:%M:%S')



date_s_date('2020-01-01T16:00:00.000Z')