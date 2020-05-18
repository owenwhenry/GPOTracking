# -*- coding: utf-8 -*-
"""
Created on Sat May  9 20:54:06 2020

@author: henry
"""

import requests as req
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import setup.config as config
from setup.db_setup import (Base, runStats)
from db_factory import db_factory
import logging


class runner:
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.engine = create_engine('sqlite:///GPOWarehouse.sqlite', 
                                    echo = False)
        self.Base = Base
        self.Base.metadata.bind = self.engine
        self.DBSession = sessionmaker(bind=self.engine)    
    
    def get_api_data(self, url, **kwargs):
        '''
        Makes an API call to a specified URL with specified parameters, then
        returns the result as JSON. 
        
        Parameters
        ----------
        url : String
            The URL to be called, optionally including any parameters you'd
            like to have included as part of the call.
        **kwargs : Keyword arguements
            Any additional parameters you'd like to have added to the API call.
            If there are parameters included in the URL that you want to
            overwrite with your own values, include them here. 

        Returns
        -------
        json_data : JSON-formatted collections of dictionaries and lists
            Results from the API call

        '''
        params = dict()
        while url:
            query = req.utils.urlparse(url).query
            if '?' in url:
                params = dict(x.split('=') for x in query.split('&'))
            params['api_key'] = config.gov_key
            for key, value in kwargs.items():
                params[key] = value
            data = req.get(url, params=params)
            json_data = data.json()
            url = json_data['nextPage'] if 'nextPage' in json_data else None
            yield json_data
        

    def get_last_run(self, session):
        '''
        Gets a SQLAlchemy ORM object representing the last run of this program.
        Values returned include .from_date, .to_date, .run_time, and .id.

        Parameters
        ----------
        session : SQLAlchemy Session Object
            An object representing the SQLAlchemy session the call is being 
            made as a part of.

        Returns
        -------
        last_run : SQLAlchemy ORM Instance State
            An object representing a single row from the database with the
            highest run_id. Valuues of the object can be accessed by typing the
            object name and .from_date, .to_date, .run_time, and .id.
        '''
        
        max_id = session.query(func.max(runStats.id)).one()[0]
        last_run = session.query(runStats).filter(runStats.id == max_id).one()
        self.logger.debug('Last run values: %s'%last_run.__dict__)
        return last_run
        
    def load_collection(self, factory):
        self.logger.info('Loading Collection Stats...')
        data = self.get_api_data(config.collections_url)
        for item in data:
            factory.serialize('collections', item)
        
    def load_crec(self, factory):
        self.logger.info('Loading the Congressional Record...')
        data = self.get_api_data(config.crec_url.format(
            self.from_date.strftime(config.gpo_date_frmt),
            self.to_date.strftime(config.gpo_date_frmt)))
        for item in data:
            factory.serialize('package', item)
            for pack in item['packages']:
                package_summary_data = self.get_api_data(pack['packageLink'])
                factory.serialize('package_summary', package_summary_data)
            
    def load_bills(self, factory):
        self.logger.info('Loading bills...')
        data = self.get_api_data(config.bills_url.format(
            self.from_date.strftime(config.gpo_date_frmt),
            self.to_date.strftime(config.gpo_date_frmt)))
        for item in data:
            factory.serialize('package', item)
            for pack in item['packages']:
                package_summary_data = self.get_api_data(pack['packageLink'])
                factory.serialize('package_summary', package_summary_data)
                factory.serialize('members', package_summary_data)
                factory.serialize('committees', package_summary_data)
                
    
    def run(self, from_date = False, to_date = False):
        session = self.DBSession()
        
        self.from_date = from_date if from_date else self.get_last_run(session).to_date
        self.to_date = to_date if to_date else datetime.now()
        
        run_obj = runStats(from_date=self.from_date, to_date=self.to_date)
        session.add(run_obj)
        self.run_id = self.get_last_run(session).id
        
        factory = db_factory(self.run_id, session)
        
        self.load_collection(factory)
        self.load_bills(factory)
        self.load_crec(factory)
        
        session.commit()
        
    
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    run = runner()
    from_date = datetime.strptime('20200501', '%Y%m%d')
    to_date = datetime.strptime('20200517', '%Y%m%d')
    run.run(from_date = from_date, to_date=to_date)
    
#Steps to run
## Connect to the database
## Get the vars for the last run from the DB
## Set the run vars
#Update the collections
        
