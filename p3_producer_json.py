import random
from datetime import datetime
import string
from time import sleep
from json import dumps
from kafka import KafkaProducer

KAFKA_TOPIC_NAME_CONS = "p3-topic"
KAFKA_BOOTSTRAP_SERVERS_CONS = 'localhost:9092'

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS_CONS,
    value_serializer=lambda x: dumps(x).encode('utf-8')
)

if __name__ == '__main__':

    customer = {
        201: ['Aman', 'India', 'Kanpur'],
        202: ['Jaydeep', 'India', 'Mumbai'],
        203: ['Chintan', 'India', 'Surat'], 
        204: ['John', 'USA', 'New York'], 
        205: ['Trump', 'USA', 'Washington, D.C'], 
        206: ['Jack', 'Canada', 'Toronto'], 
        207: ['Bill', 'Australia', 'Sydney'], 
        208: ['Mark', 'Switzerland', 'Zurich'], 
        209: ['Adam', 'New Zealand', 'Auckland'], 
        210: ['Elon Musk', 'USA', 'Chicago']
    }
    product = {
        101: ['Bat', 'Sports'], 
        102: ['TV', 'Electronics'],
        103: ['t-shirt', 'Fashion'],
        104: ['laptop', 'Electronics'],
        105: ['charger', 'Accessories'],
        106: ['shoes', 'Fashion and Wearing'],
        107: ['earbuds', 'Sound'],
        108: ['Sofa', 'Furniture'],
        109: ['trimmer', 'Personal grooming'],
        110: ['Mobile', 'Mobiles']
    }

    payment_types_list = [
        'Card',
        'Internet Banking',
        'Other UPI Apps',
        'Wallet',
        'Google Pay',
        'Amazon Pay'
    ]

    ecommerce_website_name_list = [
        'www.myntra.com', 
        'www.amazon.com', 
        'www.flipkart.com', 
        'www.snapdeal.com', 
        'www.ebay.com',
        'www.alibaba.com',
        'www.jabong.com',
        'www.shopclues.com',
        'www.paytmmall.com',
        'www.olx.com'
    ]

    failure_reason_list = [
        "bank doesn't respond",
        'heavy load in server',
        'failed due to incorrect details',
        'this payment method is not working at this time'
    ]

    for i in range(10):
        event = dict()
        event["order_id"] = i
        event["customer_id"], customer_details = random.choice(list(customer.items()))
        event["customer_name"], event["country"], event["city"] = customer_details[0], customer_details[1], customer_details[2] 
        event["product_id"], product_details = random.choice(list(product.items()))
        event["product_name"], event["product_category"] = product_details[0], product_details[1]
        event["payment_type"] = random.choice(payment_types_list)
        event["qty"] = random.randint(1, 10)
        event["price"] = random.randint(1, 100)
        event["order_datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        event["ecommerce_website_name"] = random.choice(ecommerce_website_name_list)
        event["payment_txn_id"] = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        payment_txn_status = random.choice(['success', 'failed'])
        event["payment_txn_status"] = payment_txn_status
        if payment_txn_status == 'failed':
            event["failure_reason"] = random.choice(failure_reason_list)
        else:
            event["failure_reason"] = None

        producer.send(KAFKA_TOPIC_NAME_CONS, value=event)
        sleep(2)
        # print(event)
        # print('\n')