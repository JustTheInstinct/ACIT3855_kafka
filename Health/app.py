
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



if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/health/app_conf.yaml"
    log_conf_file = "/config/health/log_conf.yaml"
else:
    print("In Dev Environment")
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
    service_dict = {"port1":"storage", "port2":"audit", "port3":"processing", "port4":"receiver"}
    for each in service_dict:
        while retry_num <= max_retry:
            logger.info(f"Attempting to connect to {service_dict[each].value} service")
            
            try:
                requests.get(f"http://kafka1.eastus2.cloudapp.azure.com:{service_dict[each].keys}/rate")

                logger.info("Connection Established. Retrying...")
                retry_num = 9001
            except:
                time.sleep(1)
                retry_num += 1

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
    app.run(port=8120, use_reloader=False)
