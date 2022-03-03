from asyncio import events
from email.mime import base
import json, string, connexion, yaml, logging.config, logging, requests, sys, datetime, pykafka

from random import randint
from datetime import datetime
from connexion import NoContent
from logging.config import dictConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pykafka import KafkaClient

with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())


# Load log config
with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

# BASE = declarative_base()
# ENGINE = create_engine("sqlite:///reviews.sqlite")
# BASE.metadata.bind = ENGINE
# SESSION = sessionmaker(bind=ENGINE)
logger = logging.getLogger('basicLogger')

def create_review(body):
    trace_id = randint(0,sys.maxsize)
    body['trace_id'] = trace_id

    client = KafkaClient(hosts='kafka1.eastus2.cloudapp.azure.com:9092')
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()

    msg = { "type": "review",  
        "datetime" :    
           datetime.now().strftime( 
             "%Y-%m-%dT%H:%M:%S"),  
        "payload": body } 
    msg_str = json.dumps(msg) 
    producer.produce(msg_str.encode('utf-8'))

    logger.info(f"Received event POST request with trace id {body['trace_id']}")
    #value = requests.post('http://localhost:8090/create',json=body, headers={"Content-Type":"application/json"})
    
    return NoContent, 200

def rate(body):
    trace_id = randint(0,sys.maxsize)
    body['trace_id'] = trace_id

    client = KafkaClient(hosts='kafka1.eastus2.cloudapp.azure.com:9092')
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()

    msg = { "type": "rating",  
        "datetime" :    
           datetime.now().strftime( 
             "%Y-%m-%dT%H:%M:%S"),  
        "payload": body } 
    msg_str = json.dumps(msg) 
    producer.produce(msg_str.encode('utf-8'))

    logger.info(f"Received event POST request with trace id {body['trace_id']}")
    #value = requests.post('http://localhost:8090/rate',json=body, headers={"Content-Type":"application/json"})

    return NoContent, 200

app = connexion.FlaskApp(__name__, specification_dir='')

app.add_api("JustTheInstinct-ReMovie-0.1-swagger.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    # Load endpoint config


    app.run(port=8080)