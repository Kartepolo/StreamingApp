from datetime import datetime
from sqlalchemy.orm import contains_eager, deferred
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String, Boolean, Text, ForeignKey, Float, DATE, TIMESTAMP
from sqlalchemy.orm import relationship, backref
DbBase = declarative_base()

class Tweet(DbBase):
    __tablename__ = 'tweet'
    id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP, default=datetime.min)
    content = Column(Text, default=None)
    hashtag = Column(String(64), default=None)
    lat = Column(Float, default = 0.0)
    lon = Column(Float, default = 0.0)
