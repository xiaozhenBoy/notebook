import sys
test_order_file = sys.argv[1]
test_pre_file = sys.argv[2]
outfile = sys.argv[3]

fout = open(outfile, 'w')
pass_no = 0
fr = open(test_order_file)
fpre = open(test_pre_file)

for line in fr:
    items = line.strip().split()
    t = items[0]
    ttail = t.split('-')[-1]
    for disid in xrange(1, 67):
        gap = fpre.readline()
        gap = gap.strip()
        fout.write('%d,%s,%s\n' % (disid, t, gap))
        fout.flush()
fout.close()
