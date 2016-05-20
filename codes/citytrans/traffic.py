"""
"""
from timemap import timeMapping, mapDate2Week
from clustermap import loadDict
import sys

def formatTraffic(traffic_file, cluster_map_file, outfile):
    #
    distinct_id = loadDict(cluster_map_file)
    print('format traffice')
    fout = open(outfile, 'w')
    with open(traffic_file) as fin:
        for line in fin:
            items = line.strip().split('\t')
            did = distinct_id[items[0]]
            feats = []
            for t in items[1:-1]:
                ts = t.strip().split(':')
                feats.append(ts[1])
            fout.write('%d %s %d %s\n' % (did, ' '.join(feats), mapDate2Week(items[-1]), timeMapping(items[-1])))
            fout.flush()
    fout.close()

if __name__ == '__main__':
    formatTraffic(sys.argv[1], sys.argv[2], sys.argv[3])
