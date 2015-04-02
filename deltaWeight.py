import sys
from datetime import datetime

# weight file should guarantee first three columns as
# 1) id
# 2) date YYYY-MM-DD
# 3) weight
# and should be ordered by id

class Counter():
    def __init__(self):
        self.count=0

    def add(self):
        self.count+=1
        if not self.count % pow(10, 4):
            print "\r" + str(self.count),

def deltas(dates, weights):
    n = len(dates)
    ans = [None for j in range(n)]
    if n > 1:
        for i in range(n):
            dist = [abs((dates[j] - dates[i]).days) for j in range(n)]
            myw = weights[:]
            dist.pop(i)
            myw.pop(i)
            temp = sorted(zip(dist, myw), key=lambda x: x[0])
            dd, dw = map(list, zip(*temp))
            dd = [str(j) for j in dd[0:10]]
            dw = [str(j) for j in dw[0:10]]
            while len(dw) < 10:
                dd.append('.')
                dw.append('.')
            ans[i] = dd + dw
    else:
        ans = [['.' for j in range(20)]]
    return ans

def splitData(string):
    line = string.split(',', 3)
    myid = line[0]
    mydate = datetime.strptime(line[1], '%Y-%m-%d').date()
    myweight = float(line[2])
    return [myid, mydate, myweight]

if __name__=='__main__':
    if len(sys.argv) != 3:
        print "usage: " + sys.argv[0] + " inputfile outputfile"
        sys.exit(1)
    infile = open(sys.argv[1])
    outfile = open(sys.argv[2], 'w')
    header = infile.readline().rstrip()
    timepoints = 10
    dt = ["deltaT_%s" % (i) for i in range(1, timepoints+1)]
    dw = ["deltaW_%s" % (i) for i in range(1, timepoints+1)]
    header = "%s,%s,%s" % (header, ','.join(dt), ','.join(dw))
    outfile.write(header+"\n")
    cnt = Counter()
    curid = None
    d = []
    w = []
    out = []
    line = infile.readline().rstrip()
    while len(line) > 1:
        (uid, date, weight) = splitData(line)
        if curid is not None and curid != uid:
            ans = deltas(d, w)
            for i in range(len(out)):
                outfile.write(out[i]+','+','.join(ans[i])+"\n")
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
        ans = deltas(d, w)
        for i in range(len(out)):
            outfile.write(out[i]+','+','.join(ans[i])+"\n")
    infile.close()
    outfile.close()
