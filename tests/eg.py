import sys

from pyspark import SparkContext, SparkConf
from fpTree import FPTree


def getFrequentItems(data,minSupport):
    singleItems = data.flatMap(lambda x: [(y,1) for y in x])
    freqItems = [x for (x,y) in
    sorted(singleItems.reduceByKey(lambda x,y: x+y)
        .filter(lambda c: c[1]>=minSupport).collect(), key=lambda x: -x[1])]
    return freqItems

def getFrequentItemsets(data,minSupport,freqItems):
    rank = dict([(index, item) for (item,index) in enumerate(freqItems)]) # Ordered list based on the freequncy of items, the first is the most appearing one , the last is not appearing too much.
    numPartitions = data.getNumPartitions()
    print(numPartitions)
    workByPartition = data.flatMap(lambda basket: genCondTransactions(basket,rank,numPartitions))
    
    print(workByPartition.collect())
    
    # emptyTree = FPTree()
    # forest = workByPartition.aggregateByKey(emptyTree,lambda tree,transaction: tree.add(transaction,1),lambda tree1,tree2: tree1.merge(tree2))
    # itemsets = forest.flatMap(lambda (partId, bonsai): bonsai.extract(minSupport, lambda x: getPartitionId(x,numPartitions) == partId))

    # frequentItemsets = itemsets.map(lambda (ranks,count): ([freqItems[z] for z in ranks],count))
    # return frequentItemsets

def genCondTransactions(basket, rank, nPartitions):
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
            output[partition] = filtered[:i+1]
    return [x for x in output.items()]

def getPartitionId(key, nPartitions):
    return key % nPartitions


if __name__=="__main__":

    APP_NAME = "FPGrowth"

    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")

    sc  = SparkContext(conf=conf)

    finput = "prova.txt"
    threshold = 0.3

    data = sc.textFile(finput).map(lambda x: [y for y in x.strip().split(' ')])

    minSupport = data.count() * threshold
    freqItems = getFrequentItems(data, minSupport)
    print(freqItems)
    getFrequentItemsets(data, minSupport, freqItems)

    # freqItemsets.saveAsTextFile(foutput)
    #End Spark
    sc.stop()