from asyncio import events
from email.mime import base
import json, string, connexion, yaml, logging.config, logging, requests, sys, datetime, pykafka, time, os

from time import sleep
from random import randint
from datetime import datetime
from connexion import NoContent
from logging.config import dictConfig
from pykafka import KafkaClient

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/reciever/app_conf.yml"
    log_conf_file = "/config/receiver/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"
with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())
# External Logging Configuration
with open('log_conf_file', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger('basicLogger')
    logger.info("App Conf File: %s" % app_conf_file)
    logger.info("Log Conf File: %s" % log_conf_file)

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

    topic = retry()
    # client = KafkaClient(hosts='kafka1.eastus2.cloudapp.azure.com:9092')
    # topic = client.topics[str.encode(app_config['events']['topic'])]
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

    topic = retry()
    # client = KafkaClient(hosts='kafka1.eastus2.cloudapp.azure.com:9092')
    # topic = client.topics[str.encode(app_config['events']['topic'])]
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

def retry():
    '''Attempts to reconnect to Database'''
    retry_num = 1
    max_retry = app_config['retries']['max']
    while retry_num <= max_retry:
        
        logger.info(f"Attempting to connect: {retry_num} out of {max_retry} retries")
        
        try:
            hostname = "%s:%d" % (app_config["events"]["hostname"],   
                                app_config["events"]["port"]) 
            client = KafkaClient(hosts=hostname)
            topic = client.topics[str.encode(app_config["events"]["topic"])]
        except:
            logger.error("Connection Terminated. Retrying...")
            time.sleep(app_config['retries']['sleep'])
        retry_num += 1
    return topic

app = connexion.FlaskApp(__name__, specification_dir='')

app.add_api("JustTheInstinct-ReMovie-0.1-swagger.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    # Load endpoint config


    app.run(port=8080)
