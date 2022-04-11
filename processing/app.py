import yaml, json, connexion, logging.config, logging, sys, swagger_ui_bundle, requests, flask_cors, os, sqlite3#, drop_tables
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



if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yaml"
    log_conf_file = "/config/log_conf.yaml"
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


if not os.path.isfile(app_config["datastore"]["filename"]):
    # code for creating the database
    connection = sqlite3.connect(app_config["datastore"]["filename"])
    c = connection.cursor()

    c.execute("""
                CREATE TABLE stats
                (
                id INTEGER PRIMARY KEY ASC NOT NULL,
                num_of_ratings INTEGER NOT NULL,
                num_of_reviews INTEGER NOT NULL,
                num_positive INTEGER NOT NULL,
                num_negative INTEGER NOT NULL,
                timestamp VARCHAR(100) NOT NULL
                )
            """)

    connection.commit()
    connection.close()

ENGINE = create_engine("sqlite:///%s" % app_config["datastore"]["filename"])
BASE.metadata.bind = ENGINE
SESSION = sessionmaker(bind=ENGINE)

num_of_ratings = 0

# Functions to handle database things

def populate_stats():
    global num_of_ratings
    logger.info("Periodic Processing Begin")
    try:
        session = SESSION()

        var = session.query(Stats).order_by(Stats.timestamp.desc()).first()
        session.close()
        stats = var.to_dict()
    except:
        stats = {"num_of_ratings":0, "num_of_reviews":0, "num_positive":0, "num_negative":0, "timestamp":datetime.now()}
    logger.info(stats)
    timestamp = datetime.strftime(stats["timestamp"], "%Y-%m-%dT%H:%M:%S")
    timestamp_date = datetime.strptime(timestamp_date, "%Y-%m-%dT%H:%M:%S")
    # timestamp = datetime.now()

    # # Calculations for incremental values.
    # #num_of_ratings += var.num_of_ratings
    # num_of_ratings = stats["num_of_ratings"] # HARD CODED FOR TESTING
    # num_positive = randint(0,num_of_ratings)
    # num_negative = num_of_ratings - num_positive

    data = requests.get(f'{app_config["eventstore"]["url"]}/create', params={"timestamp":timestamp})
    if data.status_code == 200 and len(data.json()) > 0:
        logger.info(f"{data} received on reviews")
        stats["num_of_reviews"] += len(data.json())
    # else:
    #     logger.error(f"{data} received on reviews")
    #     return 404

    data = requests.get(f'{app_config["eventstore"]["url"]}/rate', params={"timestamp":timestamp})
    if data.status_code == 200 and len(data.json()) > 0:
        logger.info(f"{data} received on ratings")
        stats["num_of_ratings"] += len(data.json())
    # else:
    #     logger.error(f"{data2} received on rate")
    #     return 404

    data = Stats(
        stats["num_of_ratings"],
        stats["num_of_reviews"],
        stats["num_positive"],
        stats["num_negative"]
        )

    logger.info("Periodic Processing End")
    session.add(data)
    session.commit()
    session.close()

def init_scheduler():
    sch = BackgroundScheduler(daemon=True)
    sch.add_job(populate_stats, 'interval', seconds=app_config['scheduler']['period_sec'])
    sch.start()

def get_stats():
    try:
        session = SESSION()
        stats = session.query(Stats).order_by(Stats.timestamp.desc()).first()
        session.close()
        return stats.to_dict(), 201
    except:
        stats = {"num_of_ratings":0, "num_of_reviews":0, "num_positive":0, "num_negative":0, "timestamp":datetime.now()}
        return stats, 201

def get_health():
    pass

app = connexion.FlaskApp(__name__, specification_dir='')
if "TARGET_ENV" not in os.environ or os.environ["TARGET_ENV"] != "test":
    CORS(app.app)
    app.app.config['CORS_HEADERS'] = 'Content-Type'

app.add_api("JustTheInstinct-ReMovie-0.1-swagger.yaml", base_path="/processing", strict_validation=True, validate_responses=True)

if __name__ == "__main__":

    # Load log config
    
    init_scheduler()
    app.run(port=8100, use_reloader=False)
