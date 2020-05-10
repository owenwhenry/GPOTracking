# -*- coding: utf-8 -*-
"""
Created on Sat May  9 20:54:06 2020

@author: henry
"""

import requests as req
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from setup.config import gov_key
from setup.db_setup import Base, RunStats, Endpoint, Collections, Package


class runner:
    
    def __init__(self):
        self.key = gov_key
        self.govinfo_root = 'https://api.govinfo.gov'
        self.engine = create_engine('sqlite:///../GPOWarehouse.sqlite', 
                                    echo = True)
        self.Base = Base
        self.Base.metadata.bind = self.engine
        self.DBSession = sessionmaker(bind=self.engine)    
    
    def get_data(self, url):
        query = req.utils.urlparse(url).query
        params = dict(x.split('=') for x in query.split('&'))
        params['api_key'] = gov_key
        data = req.get(url, params=params)
        json_data = data.json()
        return json_data
    
    def get_last_run(self, db_session):
        max_id = db_session.query(func.max(RunStats.id))
        last_run = db_session.query(RunStats).filter(RunStats.id == max_id).one()
        return last_run
    
    
    
#Steps to run
## Connect to the database
## Get the vars for the last run from the DB
## Set the last run vars
        
