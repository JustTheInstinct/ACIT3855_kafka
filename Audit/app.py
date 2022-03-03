from cgitb import reset
from distutils.log import error
import yaml, json, connexion, logging.config, logging, sys, pykafka, logging

from random import randint
from datetime import datetime
from connexion import NoContent
from logging.config import dictConfig
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread

logger = logging.getLogger('basicLogger')
logger.setLevel(logging.INFO)

with open('app_conf.yaml', 'r') as f:
    app_conf = yaml.safe_load(f.read())

with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)


def get_review(index=0):
    counter_review = 0
    hostname = "%s:%d" % (app_conf["events"]["hostname"],  
                          app_conf["events"]["port"]) 
    client = KafkaClient(hosts=hostname) 
    topic = client.topics[str.encode(app_conf["events"]["topic"])]

    sim_client = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)

    logger.info("Getting review at index: %d" % index)

    try:
        for msg in sim_client:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if msg['type'] == 'review':
                if counter_review == index:
                    return msg, 200
                else:
                    counter_review += 1

    except:
        logger.error("No messages found")
    
    logger.error("No reviews at index: %d" % index)
    
    return {"message": "Not Found"}, 404

def get_rating(index=0):
    counter_rating = 0
    hostname = "%s:%d" % (app_conf["events"]["hostname"],  
                          app_conf["events"]["port"]) 
    client = KafkaClient(hosts=hostname) 
    topic = client.topics[str.encode(app_conf["events"]["topic"])]

    sim_client = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)

    logger.info("Getting review at index: %d" % index)

    try:
        for msg in sim_client:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if msg['type'] == 'rating':
                if counter_rating == index:
                    return msg, 200
                else:
                    counter_rating += 1
    except:
        logger.error("No messages found")
    
    logger.error("No reviews at index: %d" % index)
    
    return {"message": "Not Found"}, 404

app = connexion.FlaskApp(__name__, specification_dir='')

app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    with open('log_conf.yaml', 'r') as f:
        log_config = yaml.safe_load(f.read())
        logging.config.dictConfig(log_config)
    
    with open('app_conf.yaml', 'r') as f:
        app_conf = yaml.safe_load(f.read())

    app.run(port=9092)
