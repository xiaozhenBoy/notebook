"""
According order information, generate order feature for further analysis.
"""
from clustermap import loadDict
from timemap import timeMapping

import sys, os

def simpleOrderFeat(order_file, distinct_map_file, outfile):
    """
    order_file: format refer to competition
    distinct_map_file: distinct--id mapping
    outfile:
         format: answer_or_not \t start_distict_id \t dest_distict_id \t price \t time
         answer_or_not: flag of whether the request is answered or not. 0 mean True, 1 for False
         distinct_id:
         prince:
         time:
    """
    print('Loading distinct_id ...')
    distinct_id = loadDict(distinct_map_file)

    # extract order file
    fout = open(outfile, 'w')
    except_order_no = 0
    with open(order_file) as fin:
        line_no = 0
        for line in fin:
            items = line.strip().split('\t')
            if items[1] == 'NULL':
                answer_flag = 0
            else:
                answer_flag = 1
            try:
                fout.write('%d\t%d\t%d\t%s\t%s\n' % (answer_flag, distinct_id[items[3]], distinct_id[items[4]], items[5], timeMapping(items[6])))
            except:
                except_order_no += 1
            line_no += 1
            sys.stdout.write('Processing: %d\r' % line_no)
    print
    fout.close()
    print except_order_no

if __name__ == '__main__':
    simpleOrderFeat(sys.argv[1], sys.argv[2], sys.argv[3])
