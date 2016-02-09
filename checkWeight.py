import sys
import argparse

# weight file should guarantee first four columns as
# 1) ValueID (numeric)
# 2) PatientID (numeric)
# 3) Date (yyyy-mm-dd)
# 4) Value (raw weight or other value from EHR)
# and should be ordered by PatientID, Date, Value

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

def readPatient(filename, d, bnd):
    fh = open(filename)
    # remove header
    fh.readline()
    ids = {}
    for line in fh:
        (pid, sid) = line.rstrip().split(d, 1)
        if sid not in bnd:
            print "StrataID [%s] does not exist" % (sid)
            sys.exit(-1)
        ids[pid] = sid
    fh.close()
    return ids

def readStrata(filename, d):
    fh = open(filename)
    # remove header
    fh.readline()
    bounds = {}
    for line in fh:
        (label, lb, ub) = line.rstrip().split(d, 2)
        try:
            bounds[label] = [float(lb), float(ub)]
        except ValueError:
            print "non-numeric value [%s, %s] given for lower/upper bound on strata [%s]" % (lb, ub, label)
            sys.exit(-1)
    fh.close()
    return bounds

def testBounds(val, lb, ub):
    try:
        myweight = float(val)
    except ValueError:
        return 'numeric'
    if myweight < lb:
        return 'lower'
    if myweight > ub:
        return 'upper'
    return None

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("datafile", help='delimited file with format ValueID,PatientID,Date,Value,ETC')
    parser.add_argument("stratafile", help='delimited file with format PatientID,StrataID')
    parser.add_argument("stratabounds", help='delimited file with format StrataID,LowerBound,UpperBound')
    parser.add_argument("outputfile")
    parser.add_argument("-d", "--delimiter", help='file delimiter, defaults to ","', default=',')
    parser.add_argument("--nocount", help='turn counter off', action='store_true')
    args = parser.parse_args()
    delim = args.delimiter
    # read external boundaries
    bounds = readStrata(args.stratabounds, delim)
    # read strata ids
    ids = readPatient(args.stratafile, delim, bounds.keys())
    infile = open(args.datafile)
    outfile = open(args.outputfile, 'w')
    header = infile.readline().rstrip()
    outfile.write(header+"\n")
    errBounds = open('Recoverable2.csv', 'w')
    errBounds.write(header+"\n")
    if args.nocount:
        cnt = Nothing()
    else:
        cnt = Counter()
    line = infile.readline().rstrip()
    while len(line) > 1:
        dat = line.split(delim)
        (lb, ub) = bounds[ids[dat[1]]]
        err = testBounds(dat[3], lb, ub)
        if err is None:
            outfile.write(line + "\n")
        else:
            errBounds.write(line + "\n")
        line = infile.readline().rstrip()
        cnt.add()
    infile.close()
    outfile.close()
    errBounds.close()
