
import sys
from pyspark import SparkContext, SparkConf

from operator import add
from pyspark.sql import SparkSession

############################################################################

def countMap(row):
    time = row[0]
    value = row[1]
    value = value.split(' ')
    output = []
    for item in value:
        output.append([item,[1,[int(time)]]])
    return output

def countReduce(x,y):
    return x[0]+y[0], x[1]+y[1]

def countFilter(c, minSupport, minTSupport):
    LS = max(c[1][1])-min(c[1][1])+1
    if c[1][0]/LS >= minSupport and LS >= minTSupport:
        return (c[0], (c[1][0]/LS, c[1][1]))

############################################################################

def getSortedSingleItemsList(SingleItems):
    return [x for (x,y) in sorted(SingleItems.collect(), key=lambda c: -c[1][0]/(max(c[1][1])-min(c[1][1])+1))]

############################################################################

def getSortedData(row, fList):
    time = row[0]
    value = row[1]
    value = value.split(' ')
    value = [item for item in value if item in fList] # consider only freq items
    value = sorted(value, key = lambda x: fList.index(x)) # sort desc order
    return (time, value)


def FpMap(value, fList):
    transaction = " ".join(value)
    gList = {}
    visited = {}

    print(value)

    noOfgroups = 6
    totalElements = len(fList)
    if noOfgroups >= totalElements:
        for i in range(totalElements):
            gList[fList[i]] = i+1
    else:
        elePerGroup = totalElements/noOfgroups
        for i in range(totalElements):
            groupId = (i+1)/elePerGroup
            if (i+1)%elePerGroup != 0:
                groupId += 1
            if groupId > noOfgroups:
                groupId = noOfgroups
            gList[fList[i]] = groupId

    # reorder transaction accordin to Flist
    newtansactionList = reorderTransaction(transaction, fList)

    size = len(newtansactionList)
    for j in reversed(range(size-1)):
        gid = gList[newtansactionList[j]]
        if gid not in visited:
            visited[gid] = True
            newKey = gid
            dependentTransaction = ""
            for i in range(j):
                dependentTransaction += newtansactionList[i]
                if i != j:
                    dependentTransaction += " "
            print(dependentTransaction)
            return (newKey, dependentTransaction)



def reorderTransaction(transaction, fList):
    value = transaction.split(' ')
    value = [item for item in value if item in fList] # consider only freq items
    value = sorted(value, key = lambda x: fList.index(x)) # sort desc order
    return value



############################################################################

spark = SparkSession\
        .builder\
        .appName("PythonWordCount")\
        .master("local[*]")\
        .getOrCreate()

data = spark.read.option("header", "true").csv("prova.csv")
data.show()

# print(data.rdd.map(lambda x: x).collect())

SingleItems = data.rdd.flatMap(lambda row: countMap(row)) \
                      .reduceByKey(lambda x,y: countReduce(x,y)) \
                      .filter(lambda c: countFilter(c, 0.5, 2))
print(SingleItems.collect())
print()

fList = getSortedSingleItemsList(SingleItems)
print(fList)
print()

prova = data.rdd.map(lambda row: FpMap(row[1],fList))

print(prova.collect())

# gList = data.rdd.map(lambda row: getSortedData(row, fList))
# print(gList.collect())
# print()
