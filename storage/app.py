#from httpx import request
import yaml, json, connexion, logging.config, logging, sys, pykafka#, drop_tables_mysql
#import create_database_mysql

from base import BASE
from reviews import Review
from rating import Rating

from random import randint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from connexion import NoContent
from logging.config import dictConfig
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread

ENGINE = create_engine("mysql+pymysql://user:password@kafka1.eastus2.cloudapp.azure.com:3306/events")
#ENGINE = create_engine("mysql+pymysql://root:Solomon2002!@localhost:3306/events")
BASE.metadata.bind = ENGINE
logger = logging.getLogger('basicLogger')
logger.info("Connecting to kafka1.eastus2.cloudapp.azure.com on Port 3306")
logger.setLevel(logging.DEBUG)


#drop_tables_mysql
#create_database_mysql

SESSION = sessionmaker(bind=ENGINE)

# Functions to handle database things=

def create_review(body):
    session = SESSION()
    trace_id = randint(0,sys.maxsize)
    body['trace_id'] = trace_id
    logger.info(f"Stored event POST response with trace id {body['trace_id']}")
    logger.info("Connected to kafka1.eastus2.cloudapp.azure.com on Port 3306")
    data = Review(body["review_id"],
                    body['username'],
                    body['comment'],
                    body['rating'],
                    body['timestamp'],
                    body['trace_id'])

    session.add(data)
    session.commit()
    session.close()

    return NoContent, 201

def get_review(timestamp):
    session = SESSION()

    timestamp_date = timestamp

    reviews = session.query(Review).filter(Review.timestamp >= timestamp_date)

    review_list = []

    for review in reviews:
        review_list.append(review.to_dict())
    session.close()

    logger.info("Query REVIEW after %s returns %d items" % (timestamp, len(review_list)))
    logger.info("Connected to kafka1.eastus2.cloudapp.azure.com on Port 3306")
    return review_list, 200

def rate(body):
    session = SESSION()
    trace_id = randint(0,sys.maxsize)
    body['trace_id'] = trace_id
    logger.info(f"Stored event POST response with trace id {body['trace_id']}")
    logger.info("Connected to kafka1.eastus2.cloudapp.azure.com on Port 3306")
    data = Rating(body["response_id"],
                    body['user_rating'],
                    body['rate_count'],
                    body['timestamp'],
                    body['trace_id'])

    session.add(data)
    session.commit()
    session.close()

    return NoContent, 201

def get_rating(timestamp):
    session = SESSION()

    timestamp_date = timestamp

    ratings = session.query(Rating).filter(Rating.timestamp >= timestamp_date)

    rating_list = []

    for rating in ratings:
        rating_list.append(rating.to_dict())
    session.close()

    logger.info("Query RATING after %s returns %d items" % (timestamp, len(rating_list)))
    logger.info("Connected to kafka1.eastus2.cloudapp.azure.com on Port 3306")
    return rating_list, 200

def process_messages(): 
    """ Process event messages """
    create_review
    rate
    

    hostname = "%s:%d" % (app_config["events"]["hostname"],   
                          app_config["events"]["port"]) 
    client = KafkaClient(hosts=hostname) 
    topic = client.topics[str.encode(app_config["events"]["topic"])] 
     
    consumer = topic.get_simple_consumer(consumer_group=b'event_group', 
                                         reset_offset_on_start=False, 
                                         auto_offset_reset=OffsetType.LATEST) 
 
    # This is blocking - it will wait for a new message 
    for msg in consumer: 
        msg_str = msg.value.decode('utf-8') 
        msg = json.loads(msg_str) 
        logger.info("Message: %s" % msg) 
 
        payload = msg["payload"] 
 
        if msg["type"] == "review": # Change this to your event type 
            # Store the event1 (i.e., the payload) to the DB 
            create_review(payload)
        elif msg["type"] == "rating": # Change this to your event type 
            # Store the event2 (i.e., the payload) to the DB 
            rate(payload)
 
        # Commit the new message as being read 
        consumer.commit_offsets() 

app = connexion.FlaskApp(__name__, specification_dir='')

app.add_api("JustTheInstinct-ReMovie-0.1-swagger.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    with open('app_conf.yaml', 'r') as f:
        app_config = yaml.safe_load(f.read())

    t1 = Thread(target=process_messages) 
    t1.setDaemon(True) 
    t1.start()

    # Load log config
    with open('log_conf.yaml', 'r') as f:
        log_config = yaml.safe_load(f.read())
        logging.config.dictConfig(log_config)

    app.run(port=8090)
