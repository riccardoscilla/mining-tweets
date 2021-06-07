import datetime as dt
from importCSV import importFromCSV
from TFP_Growth import fpgrowth
from TApriori import apriori
from MaxFI import maximalFrequentItemsets

import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
from report import report

import argparse
import os.path
import sys

test =  [   [1,["A","C","F","H","I"]],
            [2,["A","B","C","G"]],
            [3,["B","C","D","G","I"]],
            [4,["A","C","I"]],
            [5,["C","D","E","H","I"]],
            [6,["A","D","F","G","I"]],
            [7,["G","B","D", "I"]]
        ]

def apriori_process(inputfile, ndata, minSup, minTSup):
    tstart = dt.datetime.now()

    data = importFromCSV(inputfile,ndata)
    timport = dt.datetime.now()
    print("Import",timport-tstart)

    freqItemsets, globLS, globSup = apriori(data,minSup,minTSup[0],minTSup[1])
    tapriori= dt.datetime.now()
    print("Apriori",tapriori-timport)
    time_duration = tapriori-timport
    
    if freqItemsets:    
        MaxfreqItemsets = maximalFrequentItemsets(freqItemsets,globLS,globSup)
        tmaxFI = dt.datetime.now()
        print("Maximal FI",tmaxFI-tapriori)

    tend = dt.datetime.now()
    print("Total",tend-tstart)

    return time_duration, len(freqItemsets), len(MaxfreqItemsets)


def fp_process(inputfile, ndata, minSup, minTSup):
    tstart = dt.datetime.now()

    data = importFromCSV(inputfile,ndata)
    timport = dt.datetime.now()
    print("Import",timport-tstart)

    freqItemsets, globLS, globSup = fpgrowth(data,minSup,minTSup[0],minTSup[1])
    tfpgrowth = dt.datetime.now()
    print("FPgrowth",tfpgrowth-timport)
    time_duration = tfpgrowth-timport

    if freqItemsets:    
        MaxfreqItemsets = maximalFrequentItemsets(freqItemsets,globLS,globSup)
        tmaxFI = dt.datetime.now()
        print("Maximal FI",tmaxFI-tfpgrowth)

    tend = dt.datetime.now()
    print("Total",tend-tstart)

    return time_duration, len(freqItemsets), len(MaxfreqItemsets), MaxfreqItemsets

def single_test(inputfile,datalen, minSupList, TSupList):
    timeapriori = []
    timefpgrowth = []

    maxfreqitemsapriori = []
    maxfreqitemfpgrowth = []

    if len(datalen)>1:
        column = ["# Transactions", "Time (s)",\
                  "# Frequent Itemsets", "# Maximal Frequent Itemsets"]
    elif len(minSupList)>1:
        column = ["Support", "Time (s)",\
                  "# Frequent Itemsets", "# Maximal Frequent Itemsets"]
    elif len(TSupList)>1:
        column = ["Temporal Support", "Time (s)",\
                  "# Frequent Itemsets", "# Maximal Frequent Itemsets"]

    df1 = DataFrame(columns = column)
    df2 = DataFrame(columns = column)

    for ndata in datalen:
        for minSup in minSupList:
            for TSup in TSupList:
                tapriori, FIapriori, MFIapriori = apriori_process(inputfile,ndata, minSup, TSup)
                timeapriori.append(float(tapriori.total_seconds()))
                maxfreqitemsapriori.append(int(MFIapriori))

                tfpgrowth, FIfpgrowth, MFIfpgrowth,_ = fp_process(inputfile,ndata, minSup, TSup)
                timefpgrowth.append(float(tfpgrowth.total_seconds()))
                maxfreqitemfpgrowth.append(int(MFIfpgrowth))

                if len(TSupList)>1:
                    TSupStr = "["+str(TSup[0])+', '+str(TSup[1])+"]"
                    df1.loc[len(df1)] = [TSupStr, round(float(tapriori.total_seconds()),2),\
                                    int(FIapriori), int(MFIapriori) ]

                    df2.loc[len(df2)] = [TSupStr, round(float(tfpgrowth.total_seconds()),2),\
                                        int(FIfpgrowth), int(MFIfpgrowth) ]
            
            if len(minSupList)>1:
                df1.loc[len(df1)] = [float(minSup), round(float(tapriori.total_seconds()),2),\
                                int(FIapriori), int(MFIapriori) ]

                df2.loc[len(df2)] = [float(minSup), round(float(tfpgrowth.total_seconds()),2),\
                                    int(FIfpgrowth), int(MFIfpgrowth) ]


        if len(datalen)>1:
            df1.loc[len(df1)] = [int(ndata), round(float(tapriori.total_seconds()),2),\
                                int(FIapriori), int(MFIapriori) ]

            df2.loc[len(df2)] = [int(ndata), round(float(tfpgrowth.total_seconds()),2),\
                                int(FIfpgrowth), int(MFIfpgrowth) ]

            
                
    return timeapriori, timefpgrowth, maxfreqitemsapriori, maxfreqitemfpgrowth, df1, df2

def stats(inputfile,mode):
    rep = report()

    #################################################################
    if mode == 1:
        rep.add_title("Evaluation - Number of Transactions")

        datalen =  [1000, 5000, 10000, 50000, 100000, 150000]
        minSupList = [0.5]
        TSupList = [[3,21]]
        rep.add_parameters(datalen, minSupList, TSupList)    

        timeapriori,timefpgrowth, MFIapriori, MFIfpgrowth, df1, df2 = single_test(inputfile,datalen, minSupList, TSupList)

        rep.add_title("Apriori", level=3)
        rep.add_table(df1)

        rep.add_title("FP-Growth", level=3)
        rep.add_table(df2)

        _, ax = plt.subplots()
        ax.plot(datalen, timeapriori, label="Apriori", marker='o')
        ax.plot(datalen, timefpgrowth, label="FP-Growth", marker='o')
        ax.set(xlabel='# transactions', ylabel='time (s)')
        ax.legend()
        rep.add_plot()   
        
        _, ax2 = plt.subplots()
        width = 0.25
        x = np.arange(len(datalen))
        ax2.bar(x-width/2, MFIapriori, width, label="Apriori")
        ax2.bar(x+width/2, MFIfpgrowth, width, label="FP-Growth")
        ax2.set(xlabel='# transactions', ylabel='# Max Frequent Itemsets')
        labels = [str(d) for d in datalen]
        ax2.set_xticks(x)
        ax2.set_xticklabels(labels)
        ax2.legend()
        rep.add_plot()   
        
        rep.write("report_NumTransactions.html")

    #################################################################
    elif mode == 2:
        rep.add_title("Evaluation - Support")

        datalen =  [20000]
        minSupList = [0.5,0.7]
        TSupList = [[3,21]]
        rep.add_parameters(datalen, minSupList, TSupList)    

        timeapriori,timefpgrowth, MFIapriori, MFIfpgrowth, df1, df2 = single_test(inputfile,datalen, minSupList, TSupList)

        rep.add_title("Apriori", level=3)
        rep.add_table(df1)

        rep.add_title("FP-Growth", level=3)
        rep.add_table(df2)

        _, ax = plt.subplots()
        ax.plot(minSupList, timeapriori, label="Apriori", marker='o')
        ax.plot(minSupList, timefpgrowth, label="FP-Growth", marker='o')
        ax.set(xlabel='Support', ylabel='time (s)')
        labels = [str(d) for d in minSupList]
        ax.set_xticks(minSupList)
        ax.set_xticklabels(labels)
        ax.legend()
        rep.add_plot()

        width = 0.25
        x = np.arange(len(minSupList))
        _, ax2 = plt.subplots()
        ax2.bar(x-width/2, MFIapriori, width, label="Apriori")
        ax2.bar(x+width/2, MFIfpgrowth, width, label="FP-Growth")
        ax2.set(xlabel='Support', ylabel='# Max Frequent Itemsets')
        labels = [str(d) for d in minSupList]
        ax2.set_xticks(x)
        ax2.set_xticklabels(labels)
        ax2.legend()
        rep.add_plot()   
        
        rep.write("report_Support.html")

    #################################################################
    elif mode == 3:
        rep.add_title("Evaluation - Temporal Support")

        datalen =  [20000]
        minSupList = [0.5]
        TSupList = [[3,7], [3,14], [3,21], [3,28], [3,35]]
        rep.add_parameters(datalen, minSupList, TSupList)    

        timeapriori,timefpgrowth, MFIapriori, MFIfpgrowth, df1, df2 = single_test(inputfile,datalen, minSupList, TSupList)

        rep.add_title("Apriori", level=3)
        rep.add_table(df1)

        rep.add_title("FP-Growth", level=3)
        rep.add_table(df2)

        _, ax = plt.subplots()
        x_tick = [d[1] for d in TSupList]
        ax.plot(x_tick , timeapriori, label="Apriori", marker='o')
        ax.plot(x_tick , timefpgrowth, label="FP-Growth", marker='o')
        ax.set(xlabel='Temporal Support', ylabel='time (s)')
        labels = ["["+str(d[0])+', '+str(d[1])+"]" for d in TSupList]
        ax.set_xticks(x_tick)
        ax.set_xticklabels(labels)
        ax.legend()
        rep.add_plot()

        
        _, ax2 = plt.subplots()
        width = 0.25
        x = np.arange(len(TSupList))
        ax2.bar(x-width/2, MFIapriori, width, label="Apriori")
        ax2.bar(x+width/2, MFIfpgrowth, width, label="FP-Growth")
        ax2.set(xlabel='Temporal Support', ylabel='# Max Frequent Itemsets')
        labels = ["["+str(d[0])+', '+str(d[1])+"]" for d in TSupList]
        ax2.set_xticks(x)
        ax2.set_xticklabels(labels)
        ax2.legend()
        rep.add_plot()   
        
        rep.write("report_TemporalSupport.html")

def table_MFI(inputfile,ndata, supp, tsupp):
    rep = report()
    rep.add_title("Evaluation - Table of Maximal Frequent Itemsets")

    _,_,_,MFI = fp_process(inputfile,ndata,supp,tsupp)
    rep.add_parameters([ndata], [supp], [tsupp])    

    df = DataFrame(MFI,columns=["Topic","Timespan"])
    sample = len(MFI) if len(MFI)<30 else 30
    df = df.sample(sample) \
           .reset_index(drop=True)
    rep.add_table(df)
    rep.write("report_TableTopic.html")


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')


if __name__ == "__main__":
    # 1: Num of transactions
    # 2: Support Threshold
    # 3: Temporal Support Threshold
    modes = [1,2,3]
    parser = argparse.ArgumentParser(description='Report for Performance Evaluation')
    group = parser.add_mutually_exclusive_group()

    group.add_argument("--test", type=int, choices=modes, default=None,
                        help='Modes to run the tests: \n1. Number of transactions; 2. Support Threshold; 3. Temporal Support Threshold')

    group.add_argument("--table",  action="store_true",
                        help='Select to save Maximum Frequent Itemset Table')
    
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

    if args.test:
        stats(args.input,args.test)

    elif args.table:
        table_MFI(args.input,args.ndata,args.supp,[args.minTsupp,args.maxTsupp])

