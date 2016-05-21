"""
"""
import sys

poi_file = sys.argv[1]
weather_file = sys.argv[2]
traffic_file = sys.argv[3]
test_order_file = sys.argv[4]
outfile = sys.argv[5]

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

# generate feature
fout = open(outfile, 'w')
pass_no = 0
with open(test_order_file) as fr:
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
            fout.write('%d %s %s\n' % (disid, ttail, ' '.join(feats)))
            fout.flush()
fout.close()
print pass_no
