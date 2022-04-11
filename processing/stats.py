from xmlrpc.client import Boolean
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from base import BASE

class Stats(BASE):
    __tablename__ = "stats"

    id = Column(Integer, primary_key=True)
    num_of_ratings = Column(Integer, nullable=False)
    num_of_reviews = Column(Integer, nullable=False)
    num_positive = Column(Integer, nullable=False)
    num_negative = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    def __init__(self, num_of_ratings, num_of_reviews, num_positive, num_negative):
        self.num_of_ratings = num_of_ratings
        self.num_of_reviews = num_of_reviews
        self.num_positive = num_positive
        self.num_negative = num_negative
        self.timestamp = datetime.now()

    def to_dict(self):
        # Sends items to dictionary
        dict = {}
        dict['num_of_ratings'] = self.num_of_ratings
        dict['num_of_reviews'] = self.num_of_reviews
        dict['num_positive'] = self.num_positive
        dict['num_negative'] = self.num_negative
        dict['timestamp'] = self.timestamp

        return dict