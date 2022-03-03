from xmlrpc.client import Boolean
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from base import BASE

class Rating(BASE):
    __tablename__ = "rating"

    #id = Column(Integer, primary_key=True)
    response_id = Column(String(40), primary_key=True, nullable=False)
    user_rating = Column(Boolean, nullable=False)
    rate_count = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    trace_id = Column(Integer, nullable=True)

    def __init__(self, response_id, user_rating, rate_count, created_date, trace_id):
        self.response_id = response_id
        self.user_rating = user_rating
        self.rate_count = rate_count
        self.timestamp = datetime.now()
        self.trace_id = trace_id

    def to_dict(self):
        # Sends items to dictionary
        dict = {}
        dict['response_id'] = self.response_id
        dict['user_rating'] = self.user_rating
        dict['rate_count'] = self.rate_count
        dict['timestamp'] = self.timestamp
        dict['trace_id'] = self.trace_id

        return dict