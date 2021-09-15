# read_parquet.py

from pyspark.sql import SparkSession

if __name__ == '__main__':

    spark = SparkSession \
        .builder \
        .appName("Read parquet file from HDFS") \
        .master("local[*]") \
        .getOrCreate()

    df = spark.read.parquet('p3/output.parquet/part-00000-09cfd465-1f02-4a1c-be43-03dc4ef16aae-c000.snappy.parquet')

    df.show()