from sqlite3 import Date
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from base import BASE

class Review(BASE):
    __tablename__ = "review"

    #id = Column(Integer, primary_key=True)
    review_id = Column(String(40), primary_key=True, nullable=False)
    username = Column(String(40), nullable=False)
    comment = Column(String(5000), nullable=True)
    rating = Column(Integer, nullable=False)
    #created_date = Column(DateTime, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    trace_id = Column(Integer, nullable=True)

    def __init__(self, review_id, username, comment, rating, created_date, trace_id):
        self.review_id = review_id
        self.username = username
        self.comment = comment
        self.timestamp = datetime.now()
        self.rating = rating
        self.trace_id = trace_id

    def to_dict(self):
        # Sends items to dictionary
        dict = {}
        dict['review_id'] = self.review_id
        dict['username'] = self.username
        dict['comment'] = self.comment
        dict['rating'] = self.rating
        #dict['created_date'] = datetime.now()
        dict['timestamp'] = self.timestamp
        dict['trace_id'] = self.trace_id

        return dict