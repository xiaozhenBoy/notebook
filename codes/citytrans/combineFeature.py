"""
"""
import sys

poi_file = sys.argv[1]
weather_file = sys.argv[2]
traffic_file = sys.argv[3]
order_file = sys.argv[4]
outfile = sys.argv[5]

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
            ttail = t.split('-')[-1]
            fout.write('%s %d %s %s\n' % (gap, disid, ttail, ' '.join(feats)))
            fout.flush()
        except:
            pass_no += 1
fout.close()
print pass_no
