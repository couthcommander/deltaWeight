import sys
import argparse
import os.path
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

def checkData(string, d, lb, ub, conv):
    line = string.split(d, 3)
    try:
        mydate = datetime.strptime(line[1], '%Y-%m-%d').date()
    except ValueError:
        return [string, 'date']
    try:
        myweight = float(line[2])
    except ValueError:
        return [string, 'numeric']
    fail = None
    if myweight < lb:
        fail = 'lower'
    if myweight > ub:
        fail = 'upper'
    if conv is not None:
        if fail is not None:
            myweight = myweight * conv
            if myweight < lb or myweight > ub:
                return [string, fail]
            line[2] = str(myweight)
            string = d.join(line + ["1"])
        else:
            string = string + d + "0"
    elif fail is not None:
        return [string, fail]
    return [string, '']

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", help='delimited file with format ID,DATE,WEIGHT,ETC')
    parser.add_argument("outputfile")
    parser.add_argument("-lb", "--lowerbound", help="lower bound for weight, defaults to 0", default=0, type=float)
    parser.add_argument("-ub", "--upperbound", help="upper bound for weight, defaults to 1000", default=1000, type=float)
    parser.add_argument("-c", "--conversion", help="unit conversion multiplier", type=float)
    parser.add_argument("-d", "--delimiter", help='file delimiter, defaults to ","', default=',')
    parser.add_argument("--nocount", help='turn counter off', action='store_true')
    args = parser.parse_args()
    lb = args.lowerbound
    ub = args.upperbound
    conv = args.conversion
    delim = args.delimiter
    infile = open(args.inputfile)
    outfile = open(args.outputfile, 'w')
    header = infile.readline().rstrip()
    if conv is not None:
        header = header + delim + "converted"
    outfile.write(header+"\n")
    # create four error files
    (oname, oext) = os.path.splitext(args.outputfile)
    errDate = open(oname + "_dateErr" + oext, 'w')
    errNumeric = open(oname + "_numericErr" + oext, 'w')
    errLower = open(oname + "_lowerErr" + oext, 'w')
    errUpper = open(oname + "_upperErr" + oext, 'w')
    if args.nocount:
        cnt = Nothing()
    else:
        cnt = Counter()
    line = infile.readline().rstrip()
    while len(line) > 1:
        (line, err) = checkData(line, delim, lb, ub, conv)
        if err == 'date':
            errDate.write(line + "\n")
        elif err == 'numeric':
            errNumeric.write(line + "\n")
        elif err == 'lower':
            errLower.write(line + "\n")
        elif err == 'upper':
            errUpper.write(line + "\n")
        else:
            outfile.write(line + "\n")
        line = infile.readline().rstrip()
        cnt.add()
    infile.close()
    outfile.close()
    errDate.close()
    errNumeric.close()
    errLower.close()
    errUpper.close()
