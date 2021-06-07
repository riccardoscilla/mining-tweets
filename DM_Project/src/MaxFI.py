from pyspark.sql import SparkSession
from pandas import DataFrame

def findLSofItemset(itemSet, globLS):
    # print(itemSet)
    LS = globLS[list(itemSet)[0]]
    for item in list(itemSet)[1:]:
        LS = list(set(LS) & set(globLS[item]))
    LS = [min(LS), max(LS)]
    return LS

def computeML(cli, fredic2, globSup):
    clsu = globSup[frozenset(cli)]
    checkset = fredic2[clsu]
    for i in checkset:
        if cli != i and cli.issubset(i):
            return (0, [])
    return (0, [cli])

def reduceML(x,y):
    return x+y if len(y)>0 else x

def maximalFrequentItemsets(freqItemsets, globLS, globSup, FiMaxLen=None):
    
    if FiMaxLen:
        freqItemsets = [item for item in freqItemsets if len(item)<FiMaxLen]

    spark = SparkSession\
        .builder\
        .appName("MaxFI")\
        .master("local[*]")\
        .getOrCreate()

    rdd = spark.sparkContext.parallelize(freqItemsets)

    fredic2 = rdd.map(lambda fi: (globSup[frozenset(fi)], [fi])) \
                 .reduceByKey(lambda x,y: x+y) \
                 .sortByKey().collectAsMap()

    temp = []
    for i in fredic2:
        temp.extend(fredic2[i])
        fredic2[i] = temp

    rdd = spark.sparkContext.parallelize(freqItemsets)
    ml = rdd.map(lambda cli: computeML(cli,fredic2,globSup)) \
            .reduceByKey(lambda x,y: reduceML(x,y)).collect()[0][1]

    rdd = spark.sparkContext.parallelize(ml)
    ml = rdd.map(lambda cli: [cli, findLSofItemset(cli, globLS)]).collect()
            
    spark.stop()
    print("Number of Maximal frequent itemsets: ",len(ml))
    
    df = DataFrame(ml,columns=["Topic","Timespan"])
    sample = len(ml) if len(ml)<30 else 30
    df = df.sample(sample) \
            .reset_index(drop=True)
    print(df)
    
    return ml