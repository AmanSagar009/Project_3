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

    print('*****Streaming schema*****')
    orders_df.printSchema()

    orders_df1 = orders_df.withWatermark("timestamp", "1 minutes").selectExpr("CAST(value AS STRING)")

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

    orders_df2 = orders_df1 \
        .select(from_json(col("value"), schema).alias("data")).select('data.*')

    print('*****DataFrame Schema*****')
    orders_df2.printSchema()

    # print("==========Normal DataFrame==========")
    # od_df = orders_df2.writeStream \
    #     .format("console") \
    #     .outputMode("append") \
    #     .start()

    od_df1 = orders_df2.groupBy('city', 'payment_type') \
        .agg(count('order_id').alias("total_order"), sum(col('qty')*col('price')).alias("total_amount"))

    od_df1.printSchema()

    # od_df = od_df1.writeStream \
    #     .format('parquet') \
    #     .outputMode('append') \
    #     .option('path', '/p3') \
    #     .trigger(processingTime='20 seconds') \
    #     .start()

    od_df = od_df1.writeStream \
        .trigger(processingTime='20 seconds')\
        .outputMode("update") \
        .format("console") \
        .start()

    od_df.awaitTermination()

    # transaction_details = od_df.select('order_id', 'city', (col('qty')*(col('price'))).alias('total_price'))

    # transaction_details.printSchema()

    # print("=====Transaction DataFrame=====")
    # td_df1 = transaction_details.writeStream \
    #     .format("console") \
    #     .outputMode("append") \
    #     .start()

    # card_df = od_df.filter("payment_type == 'Card'")

    # card_producer = card_df.withColumn("key", lit(100)) \
    #     .withColumn("value", concat(card_df.select("*").filter("payment_type == 'Card'")))

    # Write key-value data from a DataFrame to a specific Kafka topic specified in an option
    # trans_detail_write_stream_1 = card_producer \
    #     .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
    #     .writeStream \
    #     .format("kafka") \
    #     .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    #     .option("topic", card_topic_name) \
    #     .trigger(processingTime='1 seconds') \
    #     .outputMode("update") \
    #     .option("checkpointLocation", "file:///home/hdoop/tmp/py_checkpoint") \
    #     .start()

    # print("==========Card DataFrame==========")
    # card_df1 = card_df.writeStream \
    #     .format("console") \
    #     .outputMode("append") \
    #     .start()

    # od_df.awaitTermination()
    # od_df2.awaitTermination()
    # td_df1.awaitTermination()
    # card_df1.awaitTermination()
    