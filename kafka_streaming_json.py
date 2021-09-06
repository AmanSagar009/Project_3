#kafka_streaming_json.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import time

kafka_topic_name = "p3-topic"
kafka_bootstrap_servers = 'localhost:9092'
card_topic_name = 'card_topic'

if __name__ == "__main__":
    print("Stream Data Processing Application Started ...")
    print(time.strftime("%Y-%m-%d %H:%M:%S"))

    spark = SparkSession \
        .builder \
        .appName("PySpark Structured Streaming with Kafka and Message Format as JSON") \
        .master("local[*]") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    # Construct a streaming DataFrame that reads from test-topic
    orders_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", kafka_topic_name) \
        .option("startingOffsets", "earliest") \
        .load()

    orders_df.printSchema()

    orders_df1 = orders_df.selectExpr("CAST(value AS STRING)")

    schema = StructType() \
        .add('order_id', IntegerType()) \
        .add('customer_id', IntegerType()) \
        .add('customer_name', StringType()) \
        .add('country', StringType()) \
        .add('city', StringType()) \
        .add('product_id', IntegerType()) \
        .add('product_name', StringType()) \
        .add('product_category', StringType()) \
        .add('payment_type', StringType()) \
        .add('qty', IntegerType()) \
        .add('price', FloatType()) \
        .add('order_datetime', StringType()) \
        .add('ecommerce_website_name', StringType()) \
        .add('payment_txn_id', StringType()) \
        .add('payment_txn_status', StringType()) \
        .add('failure_reason', StringType())

    od_df = orders_df1 \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")

    od_df.printSchema()

    od_df.writeStream \
        .format("console") \
        .outputMode("append") \
        .start() \
        .awaitTermination()
    