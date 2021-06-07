import datetime as dt
from importCSV import importFromCSV
from TFP_Growth import fpgrowth
from TApriori import apriori
from MaxFI import maximalFrequentItemsets

import argparse
import os.path
import sys

def apriori_process(inputfile, ndata, minSup, minTSup):
    tstart = dt.datetime.now()

    data = importFromCSV(inputfile,ndata)
    timport = dt.datetime.now()
    print("Import",timport-tstart)

    freqItemsets, globLS, globSup = apriori(data,minSup,minTSup[0],minTSup[1])
    tapriori= dt.datetime.now()
    print("Apriori",tapriori-timport)
    
    if freqItemsets:    
        maximalFrequentItemsets(freqItemsets,globLS,globSup)
        tmaxFI = dt.datetime.now()
        print("Maximal FI",tmaxFI-tapriori)

    tend = dt.datetime.now()
    print("Total",tend-tstart)

#################################################################

def fp_process(inputfile, ndata, minSup, minTSup):
    tstart = dt.datetime.now()

    data = importFromCSV(inputfile,ndata)
    timport = dt.datetime.now()
    print("Import",timport-tstart)

    freqItemsets, globLS, globSup = fpgrowth(data,minSup,minTSup[0],minTSup[1])
    tfpgrowth = dt.datetime.now()
    print("FPgrowth",tfpgrowth-timport)

    if freqItemsets:    
        maximalFrequentItemsets(freqItemsets,globLS,globSup)
        tmaxFI = dt.datetime.now()
        print("Maximal FI",tmaxFI-tfpgrowth)

    tend = dt.datetime.now()
    print("Total",tend-tstart)

#################################################################

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Get Consistent Topics in time')
    
    group = parser.add_mutually_exclusive_group()

    group.add_argument("--fp",  action="store_true",
                        help='Run Temporal FP-Growth')

    group.add_argument("--apriori",  action="store_true",
                        help='Run Temporal Apriori')
                        
    parser.add_argument("--input",
                        help="csv data input", default="data.csv")

    parser.add_argument("--ndata", type=int, 
                        help="Number of transactions (default 10000)", default=10000)

    parser.add_argument("--supp", type=float, 
                        help="Support Threshold (default 0.5)", default=0.5)
    
    parser.add_argument("--minTsupp", type=int, 
                        help="Minimum Temporal Support Threshold (default 3)", default=3)
    
    parser.add_argument("--maxTsupp", type=int, 
                        help="Maximum Temporal Support Threshold (default 21)", default=21)    

    args = parser.parse_args()

    if args.fp:
        fp_process(args.input,args.ndata,args.supp,[args.minTsupp,args.maxTsupp])
    elif args.apriori:
        apriori_process(args.input,args.ndata,args.supp,[args.minTsupp,args.maxTsupp])
