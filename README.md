# Power Brokers

## Project Description
Using Kafka and SparkSQL / DataFrames, process data streams of "Order Placements & Transactions" data. The data is to be generated on the fly (no file input) and pushed to a Kafka topic. Read the data from the Kafka topic and perform the following operations / processes: 1. Segregate the mode of payments like credit card, debit card, Internet banking, UPI, Wallet, Google PAY, PAYTM etc., and in each identify how many were successful and how many were failed due to what reason. 2. Determine City-wise number of orders
placed and the total amount made in each payment modes mentioned above. 3. Store the results of point #4 in a Parquet file and also display the same on the console.

# Technologies Used

* Kafka
* Python
* SparkSQL
* Spark Streaming

# Features

1. We have created a producer. It will ingest data into Kafka topic every 2 second.
2. We have created a consumer that will consume data from the topic.
3. Categorized streaming data into payment types and transaction status.
  i.e Payment types: Internet banking, UPI, Card, Wallet, Google Pay, Paytm
      Transaction status: Successful, Failed
4. We have created different topic and send data to the respective topic.
  i.e If payment types is Card then it will goes to the "card-topic"
  
5. We have done some aggregation on streaming data and append processed data into parquet file. 
  i.e Total number of orders placed in particular city

# Getting Started

1. At first, You have to install Ubuntu on Oracle Virtual Box. After Ubuntu installation, You will need Hadoop, Spark and Kafka services. You can install all of three using below link.
* Ubuntu download: https://ubuntu.com/download/desktop
* Hadoop installation: https://phoenixnap.com/kb/install-hadoop-ubuntu
* Spark installation: https://sparkbyexamples.com/spark/spark-setup-on-hadoop-yarn
* Kafka installation: https://www.tutorialkart.com/apache-kafka/install-apache-kafka-on-ubuntu

2. After installing Ubuntu and all tools open terminal in Ubuntu.

3. Clone the project at home/hdoop directory using below command.
```
git clone https://github.com/AmanSagar009/Project_3.git
```

4. You can see project_3 directory when you run command "ls".

5. Enter into the project_3 directory using "cd project_3".

6. For execution of python file you need Kafka and Zookeeper started,. You can use below command for starting Zookeeper and Kafka.

  Start Zookeeper
```
$KAFKA_HOME/bin/zookeeper-server-start.sh config/zookeeper.properties
```

  Start Kafka
```
$KAFKA_HOME/bin/kafka-server-start.sh config/server.properties
```

7. When you execute this project then you need topic. You can create topic using below command when needed.
```
$KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic <topic-name>
```

8. In  the current directory, you can see producers file and consumer file.
Below command used for execute producer file
```
python3 <producer-filename>
```
Below commands used for execute consumer file. you can use anyone from below.
```
spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8-assembly_2.11:2.4.4 <consumer-filename>
```
OR
```
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 <consumer-filename>
```

# Contributors

* Aman Sagar(AmanSagar009)
* Chintan Munjani(munjanichintan123)
* Jaydeep Lanke(jaydeep1009)
