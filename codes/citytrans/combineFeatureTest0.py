"""
"""
import sys

poi_file = sys.argv[1]
weather_file = sys.argv[2]
traffic_file = sys.argv[3]
order_arr_file = sys.argv[4]
order_file_src = sys.argv[5]
order_file = sys.argv[6]
outfile = sys.argv[7]


def findMostSimilar(seqs, target):
    #
    seqs.append(target)
    seqs.sort()
    tidx = seqs.index(target)
    if tidx > 0:
        return seqs[tidx-1]
    else:
        return seqs[tidx+1]


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
fr = open(order_file_src)
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
        ttail = t.split('-')[-1]
        for disid in xrange(1, 67):
            feats = []
            feats.extend(disid_poi[disid])
            try:
                feats.extend(timeid_weather[t])
            except:
                feats.extend(timeid_weather[findMostSimilar(timeid_weather.keys(), t)])
            try:
                feats.extend(time_disid_traff[t][disid])
            except:
                tsmi = findMostSimilar(time_disid_traff.keys(), t)
                if disid not in time_disid_traff[tsmi]:
                    tdisid = findMostSimilar(time_disid_traff[tsmi].keys(), disid)
                else:
                    tdisid = disid
                feats.extend(time_disid_traff[tsmi][tdisid])
            # feats.extend(order_disid_arr[t][disid])
            ts = t.split('-')
            ttail = ts[-1]
            ttail_d = int(ts[-1])
            date = int(ts[-2])
            mouth = int(ts[-3])
            realated_t = []
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
            fout.write('%d %s %s\n' % (disid, ttail, ' '.join(feats)))
            fout.flush()

fout.close()
print pass_no
