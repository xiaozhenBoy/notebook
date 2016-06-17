"""
"""
import sys

poi_file = sys.argv[1]
weather_file = sys.argv[2]
traffic_file = sys.argv[3]
order_arr_file = sys.argv[4]
order_file = sys.argv[5]
outfile = sys.argv[6]

# load poi
print('Loading poi ...')
disid_poi = {}
with open(poi_file) as fpoi:
    for line in fpoi:
        items = line.strip().split()
        disid_poi[int(items[0])] = items[1:]

# load weather infor, with time
print('Loading weather ...')
timeid_weather = {}
with open(weather_file) as fwea:
    for line in fwea:
        items = line.strip().split()
        timeid_weather[items[0]] = items[1:]

# load traffic infor
print('Loading traffic ...')
time_disid_traff = {}
with open(traffic_file) as ft:
    for line in ft:
        items = line.strip().split()
        if items[-1] not in time_disid_traff:
            time_disid_traff[items[-1]] = {}
        time_disid_traff[items[-1]][int(items[0])] = items[1:-1]

# load traffic infor
print('Loading order...')
order_disid = {}
fr = open(order_file)
for line in fr:
    items = line.strip().split()
    if items[0] not in order_disid:
        order_disid[items[0]] = {}
    order_disid[items[0]][int(items[1])] = items[2:]
fr.close()
print('Loading order arr ...')
order_disid_arr = {}
fr = open(order_arr_file)
for line in fr:
    items = line.strip().split()
    if items[0] not in order_disid_arr:
        order_disid_arr[items[0]] = {}
    order_disid_arr[items[0]][int(items[1])] = items[2:]
fr.close()
# generate feature
fout = open(outfile, 'w')
pass_no = 0
with open(order_file) as fr:
    for line in fr:
        items = line.strip().split()
        t = items[0]
        disid = int(items[1])
        gap = items[-1]
        feats = []
        try:
            feats.extend(disid_poi[disid])
            feats.extend(timeid_weather[t])
            feats.extend(time_disid_traff[t][disid])
            # feats.extend(order_disid_arr[t][disid])
            ts = t.split('-')
            ttail = ts[-1]
            ttail_d = int(ts[-1])
            date = int(ts[-2])
            mouth = int(ts[-3])
            realated_t = []
            # more features
            if ttail_d >= 4:
                n_ts = ts[:3]
                n_ts.append('%d'%(ttail_d-1))
                realated_t.append('-'.join(n_ts))
                n_ts = ts[:3]
                n_ts.append('%d'%(ttail_d-2))
                realated_t.append('-'.join(n_ts))
                n_ts = ts[:3]
                n_ts.append('%d'%(ttail_d-3))
                realated_t.append('-'.join(n_ts))
            else:
                if ttail_d >= 3:
                    n_ts = ts[:3]
                    n_ts.append('%d'%(ttail_d-1))
                    realated_t.append('-'.join(n_ts))
                    n_ts = ts[:3]
                    n_ts.append('%d'%(ttail_d-2))
                    realated_t.append('-'.join(n_ts))
                    if (date - 1) > 0:
                        n_ts = ts[:2]
                        if (date - 1) < 10:
                            n_ts.append('0%d'%(date-1))
                        else:
                            n_ts.append('%d'%(date-1))
                        n_ts.append('%d'%144)
                        realated_t.append('-'.join(n_ts))
                    else:
                        realated_t.append('NULL')
                elif ttail_d >=2:
                    n_ts = ts[:3]
                    n_ts.append('%d'%(ttail_d-1))
                    realated_t.append('-'.join(n_ts))
                    if (date - 1) > 0:
                        n_ts = ts[:2]
                        if (date - 1) < 10:
                            n_ts.append('0%d'%(date-1))
                        else:
                            n_ts.append('%d'%(date-1))
                        temp = n_ts # n_ts.append('%d'%144)
                        realated_t.append('-'.join(temp.append('%d'%144)))
                        realated_t.append('-'.join(n_ts.append('%d'%143)))
                    else:
                        realated_t.append('NULL')
                        realated_t.append('NULL')
                else:
                    if (date - 1) > 0:
                        n_ts = ts[:2]
                        if (date - 1) < 10:
                            n_ts.append('0%d'%(date-1))
                        else:
                            n_ts.append('%d'%(date-1))
                        temp = n_ts
                        realated_t.append('-'.join(temp.append('%d'%144)))
                        temp = n_ts
                        realated_t.append('-'.join(temp.append('%d'%143)))
                        realated_t.append('-'.join(temp.append('%d'%142)))
                    else:
                        realated_t.append('NULL')
                        realated_t.append('NULL')
                        realated_t.append('NULL')
                    pass
            # add extend feature
            for rt in realated_t:
                try:
                    feats.extend(timeid_weather[rt])
                except:
                    feats.extend(['0'] * 3)
                try:
                    feats.extend(time_disid_traff[rt][disid])
                except:
                    feats.extend(['0'] * 5)
                try:
                    feats.extend(order_disid_arr[rt][disid])
                except:
                    feats.extend(['0']*2)
                try:
                    feats.extend(order_disid[rt][disid])
                except:
                    feats.extend(['0'] * 3)
            fout.write('%s %d %s %s\n' % (gap, disid, ttail, ' '.join(feats)))
            fout.flush()
        except:
            pass_no += 1
fout.close()
print pass_no
