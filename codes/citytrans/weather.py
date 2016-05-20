"""
"""
from timemap import timeMapping
import sys

def formatWeather(weather_file, outfile):
    #
    print('format weather')
    fout = open(outfile, 'w')
    with open(weather_file) as fin:
        for line in fin:
            items = line.strip().split('\t')
            feats = []
            fout.write('%s %s %s %s\n' % (timeMapping(items[0]), items[1], items[2], items[3]))
            fout.flush()
    fout.close()

if __name__ == '__main__':
     formatWeather(sys.argv[1], sys.argv[2])
