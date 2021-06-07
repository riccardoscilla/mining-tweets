# from pyspark import SparkContext
# from pyspark.sql import SQLContext

# sc = SparkContext('local','example')  # if using locally
# sql_sc = SQLContext(sc)
# dfs = sql_sc.read.option("header", "true").csv("prova.csv")

# dfs.show()

# # from pyspark import SparkContext, SparkConf

# # conf = SparkConf().setAppName("DMProject").setMaster("local")
# # sc = SparkContext(conf=conf)

# # data = sc.textFile('prova.csv')

# # print(type(data))

# count_rdd = dfs.select("words").rdd.flatMap(lambda x: x[0].split(' ')) \
#               .map(lambda x: (x, 1)).reduceByKey(lambda x,y: x+y)


import sys
from pyspark import SparkContext, SparkConf

from operator import add
from pyspark.sql import SparkSession  
from fpTree import FPTree

def getFrequentItems(data,minSupport,minTSupport):

    SingleItems = data.flatMap(lambda x: [(y, (1,[int(x[0])])) for y in x[1].split(' ')]) \
                        .reduceByKey(lambda x,y: (x[0]+y[0],x[1]+y[1])) \
                        .filter(lambda c: c[1][0]/(max(c[1][1])-min(c[1][1])+1) >= minSupport  \
                                        and (max(c[1][1])-min(c[1][1])+1) >= minTSupport)
    # print(SingleItems.collect())

    freqItems = [x for (x,y) in sorted(SingleItems.collect(), key=lambda c: -c[1][0]/(max(c[1][1])-min(c[1][1])+1))]
    # print(freqItems)

    return freqItems

def getFrequentItemsets(data, minSupport, minTSupport, freqItems):
    rank = dict([(index, item) for (item,index) in enumerate(freqItems)])
    print(rank)
    numPartitions = data.getNumPartitions()
    print(numPartitions)
    workByPartition = data.flatMap(lambda basket: genCondTransactions(basket[0],basket[1],rank,numPartitions))

    print()
    print(workByPartition.collect())

    emptyTree = FPTree()
    forest = workByPartition.aggregateByKey(emptyTree,lambda tree,transaction: tree.add(transaction, 1),lambda tree1,tree2: tree1.merge(tree2))

    print()
    print(forest.collect())

    itemsets = forest.flatMap(lambda bonsai: lambda x: print(x))

    # itemsets = forest.flatMap(lambda bonsai: bonsai[1].extract(minSupport, lambda x: getPartitionId(x[1],numPartitions) == bonsai[0]))

    print()
    print(itemsets.collect())

    # frequentItemsets = itemsets.map(lambda ranks,count: ([freqItems[z] for z in ranks],count))

    # print(frequentItemsets.collect())


def genCondTransactions(time, basket, rank, nPartitions):
    #translate into new id's using rank
    filtered = [rank[x] for x in basket if x in rank]
    #sort basket in ascending rank
    filtered = sorted(filtered)
    #subpatterns to send to each worker. (part_id, basket_slice)
    output = {}
    for i in range(len(filtered)-1, -1, -1):
        item = filtered[i]
        partition = getPartitionId(item, nPartitions)
        if partition not in output:
            output[partition] = [time, filtered[:i+1]]

    return [x for x in output.items()]


def getPartitionId(key, nPartitions):
    return key % nPartitions

if __name__=="__main__":
    conf = SparkConf().setAppName("DM_Project")
    conf = conf.setMaster("local[*]")

    sc = SparkContext(conf=conf)

    input_file = "prova.csv"
    data = sc.textFile(input_file,2) \
            .map(lambda line: line.split(',')) \
            .map(lambda line: [int(line[0]), line[1]] )

    minSupport = data.count() * 0.5
    freqItems = getFrequentItems(data, 0.5, 2)
    print(freqItems)

    getFrequentItemsets(data, 0.5, 7, freqItems)

    sc.stop()

    # spark = SparkSession\
    #     .builder\
    #     .appName("PythonWordCount")\
    #     .master("local[*]")\
    #     .getOrCreate()

    # data = spark.read.option("header", "true").csv("prova.csv")
    # data.show()

    # freqItems = getFrequentItems(data.rdd, 0.5, 2)
    # getFrequentItemsets(data.rdd, 0.5, 2, freqItems)
    

    # spark.stop()
    
