# -*- coding: utf-8 -*-
"""
Created on Sat May  9 21:32:34 2020

@author: henry
"""

from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, BigInteger, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
    
class RunStats(Base):
    __tablename__ = 'run_stats'
    id = Column(Integer, primary_key=True)
    from_date = Column(DateTime(), nullable=True)
    to_date = Column(DateTime(), nullable=False)
    run_time = Column(BigInteger, nullable=True)

class Endpoint(Base):
    __tablename__ = 'endpoints'
    id = Column(Integer, primary_key=True)
    endpoint_name = Column(String(25), nullable=False)
    endpoint_uri = Column(String(10), nullable=False)
    
class Collections(Base):
    __tablename__ = 'collections'
    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey('run_stats.id'), nullable=False)
    collection_code = Column(String(100), nullable=False)
    collection_name = Column(String(100), nullable=False)
    package_count = Column(BigInteger, nullable=False)
    granule_count = Column(BigInteger, nullable=True)

class Package(Base):
    __tablename__ = 'package'
    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey('run_stats.id'), nullable=False)
    collection_code = Column(String(100), nullable=False)
    package_type = Column(String(10), nullable=False)
    package_name = Column(String(100), nullable=False)
    package_link = Column(String(100), nullable=False)
    doc_class = Column(String(20), nullable=True)
    title = Column(String(510), nullable = False)
    congress = Column(Integer, nullable=True)


engine = create_engine('sqlite:///../GPOWarehouse.sqlite')

Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(engine)
session = DBSession()
    
base_runstat = RunStats(to_date = datetime.now())

session.add(base_runstat)
session.commit()
session.close()

    