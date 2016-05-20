"""
Loading cluster-id map, return a cluster2id dict.
"""

def loadDict(mapfile):
    """
    Mapfile format: name \t id
    """
    name2id_dict = {}
    with open(mapfile) as f:
        for line in f:
            items = line.strip().split('\t')
            name2id_dict[items[0]] = int(items[1])
    return name2id_dict
