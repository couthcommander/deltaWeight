import sys
import argparse
from datetime import datetime

# weight file should guarantee first three columns as
# 1) id
# 2) date YYYY-MM-DD
# 3) weight
# and should be ordered by id

class Counter():
    def __init__(self):
        self.count = 0

    def add(self):
        self.count += 1
        if not self.count % 10000:
            print "\r" + str(self.count),

class Nothing():
    def __init__(self):
        pass

    def add(self):
        pass

def deltas(dates, weights, m):
    n = len(dates)
    ans = [None for j in range(n)]
    if n > 1:
        for i in range(n):
            dist = [(dates[j] - dates[i]).days for j in range(n)]
            myw = [weights[j] - weights[i] for j in range(n)]
            dist.pop(i)
            myw.pop(i)
            temp = sorted(zip(dist, myw), key=lambda x: abs(x[0]))
            dd, dw = map(list, zip(*temp))
            dd = [str(j) for j in dd[0:10]]
            dw = [str(j) for j in dw[0:10]]
            while len(dw) < 10:
                dd.append(m)
                dw.append(m)
            ans[i] = dd + dw
    else:
        ans = [[m for j in range(20)]]
    return ans

def splitData(string, d):
    line = string.split(d, 3)
    myid = line[0]
    mydate = datetime.strptime(line[1], '%Y-%m-%d').date()
    myweight = float(line[2])
    return [myid, mydate, myweight]

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", help='delimited file with format ID,DATE,WEIGHT,ETC')
    parser.add_argument("outputfile")
    parser.add_argument("-d", "--delimiter", help='file delimiter, defaults to ","', default=',')
    parser.add_argument("-m", "--missing", help='missing value, defaults to "."', default='.')
    parser.add_argument("--nocount", help='turn counter off', action='store_true')
    args = parser.parse_args()
    delim = args.delimiter
    missing = args.missing
    infile = open(args.inputfile)
    outfile = open(args.outputfile, 'w')
    timepoints = 10
    dt = ["deltaT_%s" % (i) for i in range(1, timepoints+1)]
    dw = ["deltaW_%s" % (i) for i in range(1, timepoints+1)]
    header = delim.join([infile.readline().rstrip()] + dt + dw)
    outfile.write(header+"\n")
    if args.nocount:
        cnt = Nothing()
    else:
        cnt = Counter()
    curid = None
    d = []
    w = []
    out = []
    line = infile.readline().rstrip()
    while len(line) > 1:
        (uid, date, weight) = splitData(line, delim)
        if curid is not None and curid != uid:
            ans = deltas(d, w, missing)
            for i in range(len(out)):
                outfile.write(delim.join([out[i]] + ans[i]) + "\n")
            d = [date]
            w = [weight]
            out = [line]
        else:
            d.append(date)
            w.append(weight)
            out.append(line)
        curid = uid
        line = infile.readline().rstrip()
        cnt.add()
    if len(out):
        ans = deltas(d, w, missing)
        for i in range(len(out)):
            outfile.write(delim.join([out[i]] + ans[i]) + "\n")
    infile.close()
    outfile.close()
