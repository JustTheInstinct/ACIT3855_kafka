import yaml, json, connexion, logging.config, logging, sys, swagger_ui_bundle, requests, flask_cors, os, sqlite3, time#, drop_tables
#import create_tables

from base import BASE

from random import randint
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pykafka import KafkaClient
from pykafka.common import OffsetType
from connexion import NoContent
from logging.config import dictConfig
from apscheduler.schedulers.background import BackgroundScheduler



# if ("TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test") and os.path.exists('/config'):
#     print("In Test Environment")
#     app_conf_file = "/config/processing/app_conf.yaml"
#     log_conf_file = "/config/processing/log_conf.yaml"
# else:
#     print("In Dev Environment")
#     app_conf_file = "app_conf.yaml"
#     log_conf_file = "log_conf.yaml"

app_conf_file = "app_conf.yaml"
log_conf_file = "log_conf.yaml"

with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())

with open(log_conf_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')
logger.setLevel(logging.DEBUG)

def check_health():
    retry_num = 1
    max_retry = 5
    while retry_num <= max_retry:
        
        logger.info(f"Attempting to connect to: {retry_num} out of {max_retry} retries")
        
        try:
            hostname = "%s:%d" % (app_config["events"]["hostname"],   
                                app_config["events"]["port"]) 
            client = KafkaClient(hosts=hostname)
            topic = client.topics[str.encode(app_config["events"]["topic"])]
            retry_num = 9001
        except:
            logger.error("Connection Terminated. Retrying...")
            time.sleep(1)
            retry_num += 1
    return topic

def init_scheduler():
    sch = BackgroundScheduler(daemon=True)
    sch.add_job(check_health, 'interval', seconds=app_config['scheduler']['period_sec'])
    sch.start()

def get_health():
    check_health

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'

app.add_api("JustTheInstinct-ReMovie-0.1-swagger.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":

    # Load log config
    
    init_scheduler()
    app.run(port=8100, use_reloader=False)
