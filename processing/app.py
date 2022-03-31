import yaml, json, connexion, logging.config, logging, sys, swagger_ui_bundle, requests, flask_cors, os#, drop_tables
#import create_tables

from base import BASE
from stats import Stats

from random import randint
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from connexion import NoContent
from logging.config import dictConfig
from apscheduler.schedulers.background import BackgroundScheduler



#drop_tables
#if not create_tables:
#    create_tables
if not os.path.exists('data'):
    os.makedirs('data')

with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())

ENGINE = create_engine("sqlite:///%s" % app_config["datastore"]["filename"])
BASE.metadata.bind = ENGINE
SESSION = sessionmaker(bind=ENGINE)

num_of_ratings = 0

# Functions to handle database things

def populate_stats():
    global num_of_ratings
    logger.info("Periodic Processing Begin")
    trace_id = randint(0,9999999)
    session = SESSION()

    var = session.query(Stats).order_by(Stats.timestamp.desc()).first()
    logger.info(var.num_of_ratings)

    timestamp = datetime.now()

    # Calculations for incremental values.
    num_of_ratings += var.num_of_ratings
    num_of_ratings = 1000 # HARD CODED FOR TESTING
    num_positive = randint(0,num_of_ratings)
    num_negative = num_of_ratings - num_positive

    data = requests.get('http://kafka1.eastus2.cloudapp.azure.com:8090/create' + "&end_time=", params={'timestamp':"1999-02-20"})
    if data.ok:
        logger.info(f"{data} received on reviews")
    else:
        logger.error(f"{data} received on rate")
        return 404

    data2 = requests.get('http://kafka1.eastus2.cloudapp.azure.com:8090/rate' + '&end_time=', params={'timestamp':"1999-02-20"})
    if data.ok:
        logger.info(f"{data2} received on rate")
    else:
        logger.error(f"{data2} received on rate")
        return 404

    data = Stats(
        num_of_ratings,
        num_positive,
        num_negative,
        timestamp,
        trace_id)

    logger.info("Periodic Processing End")
    session.add(data)
    session.commit()
    session.close()
    pass

def init_scheduler():
    sch = BackgroundScheduler(daemon=True)
    sch.add_job(populate_stats, 'interval', seconds=app_config['scheduler']['period_sec'])
    sch.start()

def get_stats():
    session = SESSION()
    
    try:
        stats = session.query(Stats).order_by(Stats.timestamp.desc()).first()
    except:
        return NoContent, 400

    session.close()

    return stats.to_dict(), 201

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'

app.add_api("JustTheInstinct-ReMovie-0.1-swagger.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":

    # Load log config
    with open('log_conf.yaml', 'r') as f:
        log_config = yaml.safe_load(f.read())
        logging.config.dictConfig(log_config)

    logger = logging.getLogger('basicLogger')
    logger.setLevel(logging.DEBUG)

    init_scheduler()
    app.run(port=8100, use_reloader=False)
