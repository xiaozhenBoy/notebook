"""
map time to a time_id
"""
import time, datetime

def timeMapping(input_time, sep_minutes=10):
    """
    input_time: time should be format.
              format: 2016-01-01 23:30:22
    sep_minutes: cut standard of time, option [5, 10]
    output: 2016-01-01-timeid (1,2,3 )
    """
    items = input_time.strip().split()
    assert len(items) == 2
    curr_date = items[0]
    # According sep_minutes, map time to id.
    hour_inc = int(60. / sep_minutes)
    ts = items[1].strip().split(':')
    assert len(ts) == 3
    h = int(ts[0])
    m = int(ts[1])
    tid = h * hour_inc + (m + sep_minutes - 1) / sep_minutes
    return '%s-%d' % (curr_date, tid)

def mapDate2Week(intime):
    d = datetime.datetime.strptime(intime,'%Y-%m-%d %H:%M:%S')
    wday = d.weekday()
    return wday
