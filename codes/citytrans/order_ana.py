"""
Get request and answer number
"""
import sys

def countNumOfRequestAnswer(order_format_file, outfile):
    #
    timeid_requests = {}
    timeid_answers = {}
    with open(order_format_file) as fin:
        line_no = 0
        for line in fin:
            line_no += 1
            items = line.strip().split('\t')
            if items[-1] not in timeid_requests:
                timeid_requests[items[-1]] = [0] * 66
            if items[-1] not in timeid_answers:
                timeid_answers[items[-1]] = [0] * 66
            disid = int(items[1])
            if items[0] == '1':
                timeid_answers[items[-1]][disid-1] += 1
            timeid_requests[items[-1]][disid-1] += 1
            sys.stdout.write('Processing: %d\r' % line_no)
    #
    print
    fout = open(outfile, 'w')
    for key in timeid_requests.keys():
        requests = timeid_requests[key]
        answers = timeid_answers[key]
        for did in range(66):
            fout.write('%s %d %d %d %d\n' % (key, did+1, requests[did], answers[did], requests[did]-answers[did]))
    fout.close()

def countNumofReach(order_format_file, outfile):
    #
    timeid_dest = {}
    with open(order_format_file) as fin:
        line_no = 0
        for line in fin:
            line_no += 1
            items = line.strip().split('\t')
            if items[-1] not in timeid_dest:
                timeid_dest[items[-1]] = {}
            disid = int(items[2])
            if items[0] == '1':
                if disid-1 not in timeid_dest[items[-1]]:
                    timeid_dest[items[-1]][disid-1] = []
            sys.stdout.write('Processing: %d\r' % line_no)
    #
    print
    fout = open(outfile, 'w')
    for key in timeid_dest.keys():
        dest_dist = timeid_dest[key]
        for did in range(66):
            fout.write('%s %d %d %0.6f \n' % (key, did+1, len(dest_dist), sum(dest_dist)/len(dest_dist)) )
    fout.close()

if __name__ == '__main__':
    countNumOfRequestAnswer(sys.argv[1], sys.argv[2])
    # countNumofReach(sys.argv[1], sys.argv[2])
