"""
pio info ana and mapping
(1) get feature-id map
(2) format feature
"""
from clustermap import loadDict
import sys

def featureStaAndMap(pio_file, feature_map_file):
    feat_count = {}
    # count feature
    print("Statisting Feature ...")
    with open(pio_file) as f:
        for line in f:
            items = line.strip().split('\t')
            for feat in items[1:]:
                fs = feat.strip().split(':')
                assert len(fs) == 2
                if fs[0] not in feat_count:
                    feat_count[fs[0]] = 0
                feat_count[fs[0]] += 1
    # map feature to feat_id
    print('Feature Number', len(feat_count))
    feats = feat_count.keys()
    feats.sort()
    fout = open(feature_map_file, 'w')
    for idx, feat in enumerate(feats):
        fout.write('%s\t%d\n' % (feat, idx))
    fout.close()

def formatPioFeat(pio_file, feature_map_file, cluster_map_file, outfile):
    """
    map pio info to formated vector
    pio_file: pio info (\t seperator)
    feature_map_file: feature feat_id
    outfile:
    """
    print('Loading feat_id and cluster_id ...')
    feat_id = loadDict(feature_map_file)
    cluster_id = loadDict(cluster_map_file)

    feat_num = len(feat_id)
    fout = open(outfile, 'w')
    with open(pio_file) as fin:
        for line in fin:
            items = line.strip().split('\t')
            cid = cluster_id[items[0]]
            feats = [0] * feat_num
            for feat in items[1:]:
                fs = feat.strip().split(':')
                assert len(fs) == 2
                fid = feat_id[fs[0]]
                fvalue = int(fs[1])
                feats[fid] = fvalue
            fout.write('%d %s\n' % (cid, ' '.join(['%d' % v for v in feats])) )
            fout.flush()
    fout.close()

if __name__ == '__main__':
    op = sys.argv[1]
    if op == 'sta':
        featureStaAndMap(sys.argv[2], sys.argv[3])
    else:
        formatPioFeat(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
