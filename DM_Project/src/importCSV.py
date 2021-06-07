from pyspark.sql import SparkSession
from random import sample, seed

def importFromCSV(input_file, n=None):
    spark = SparkSession\
        .builder\
        .appName("ImportData")\
        .master("local[*]")\
        .getOrCreate()

    data = spark.read.option("header", "true").csv(input_file) \
                .rdd.map(lambda line: [int(line[0]), line[1].split(" ")])

    seed(10)
    if n<data.count():
        data = sample(data.collect(),n)  
    else:
        data = data.collect()

    spark.stop()  
    return data