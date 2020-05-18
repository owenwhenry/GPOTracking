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


#Facts
    
class runStats(Base):
    __tablename__ = 'run_stats'
    id = Column(Integer, primary_key=True)
    from_date = Column(DateTime(), nullable=True)
    to_date = Column(DateTime(), nullable=False)
    run_time = Column(BigInteger, nullable=True)

class endpoint(Base):
    __tablename__ = 'endpoints'
    id = Column(Integer, primary_key=True)
    endpoint_name = Column(String(25), nullable=False)
    endpoint_uri = Column(String(10), nullable=False)
    
#Dimensions
    
class collections(Base):
    __tablename__ = 'collections'
    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey('run_stats.id'), nullable=False)
    collection_code = Column(String(100), nullable=False)
    collection_name = Column(String(100), nullable=False)
    package_count = Column(BigInteger, nullable=False)
    granule_count = Column(BigInteger, nullable=True)

class package(Base):
    __tablename__ = 'package'
    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey('run_stats.id'), nullable=False)
    package_id = Column(String(50), nullable=False)
    last_modified = Column(DateTime(), nullable=False)
    package_link = Column(String(100), nullable=False)
    doc_class = Column(String(20), nullable=True)
    title = Column(String(510), nullable = False)
    congress = Column(Integer, nullable=True)
    date_issued = Column(DateTime())
    
class packageSummary(Base):
    __tablename__ = 'package_summary'
    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey('run_stats.id'), nullable=False)
    package_id = Column(String(50), ForeignKey(package.package_id), nullable=False)
    title = Column(String(510), nullable = False)
    collection_code = Column(String(10))
    collection_name = Column(String(50))
    category = Column(String(50))
    date_issued = Column(DateTime())    
    details_link = Column(String(100))
    
class committees(Base):
    __tablename__ = 'committees'
    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey('run_stats.id'), nullable=False) 
    package_id = Column(String(50), ForeignKey(package.package_id), nullable=False)
    chamber = Column(String(6))
    committee_type = Column(String(6))
    committee_name = Column(String(50))
    
class members(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    run_id = Column(Integer, ForeignKey('run_stats.id'), nullable=False) 
    package_id = Column(String(50), ForeignKey(package.package_id), nullable=False)
    member_name = Column(String(50))
    bioguide_id = Column(String(25))
    chamber = Column(String(1))
    party = Column(String(1))
    role = Column(String(15))
    state = Column(String(2))
    congress = Column(Integer)
    authority_id = Column(Integer)
        

if __name__ == '__main__':
    engine = create_engine('sqlite:///../GPOWarehouse.sqlite')
    
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBSession = sessionmaker(engine)
    session = DBSession()
        
    base_runstat = runStats(to_date = datetime.now())
    
    session.add(base_runstat)
    session.commit()
    session.close()

    