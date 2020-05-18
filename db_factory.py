# -*- coding: utf-8 -*-
"""
Created on Sat May 16 12:22:52 2020

@author: henry
"""
from datetime import datetime
from setup.config import gpo_date_frmt
from setup.db_setup import (collections, package, packageSummary, committees, 
                            members)
import logging

class db_factory:

    
    def __init__(self, run_id, session):
        self.logger = logging.getLogger(__name__)
        self.run_id = run_id
        self.session = session 
        
    def serialize(self, target_table, api_data):
        '''
        Factory method for turning gov_info API data into objects ready for 
        insertion in the database. Passes api_data values to various 
        serialization functions, which are all generators. 

        Parameters
        ----------
        target_table : String
            Value corresponding to the table name that data is to be inserted in 
        api_data : JSON object
            Data returned from an API call in JSON format
            
        Returns
        -------
        None.
        '''
        self.logger.debug('Attempting to serialize object %s to %s'%(api_data, 
                                                                    target_table))
        if target_table == 'collections':
            self.logger.debug('Assigning to collections table.')
            self.collections(api_data)
            
        if target_table == 'package':
            self.logger.debug('Assigning to package table.')
            self.packages(api_data)
        
        if target_table == 'package_summary':
            self.logger.debug('Assigning to package_summary table.')
            self.package_summaries(api_data)
            
        if target_table == 'members':
            self.logger.debug('Assigning to members table.')
            self.members(api_data)
        
        if target_table == 'committees':
            self.logger.debug('Assigning to committees table.')
            self.committees(api_data)
            
    def collections(self, collections_data):
        '''
        Generator yielding one item_dict per item in the API response

        Parameters
        ----------
        collections_data : JSON
            API response from the collection endpoint of govInfo

        Returns
        -------
        None.
        '''
        self.logger.info("Writing to 'collections' table")
        for item in collections_data['collections']:
            self.logger.debug("Serializing item: %s"%item)
            item_dict = {
                'run_id' : self.run_id,
                'collection_code' : item['collectionCode'],
                'collection_name' : item['collectionName'],
                'package_count' : item['packageCount'],
                'granule_count' : item['granuleCount'], 
                }
            self.logger.debug("Inserting item: %s"%item_dict)
            insert_object = collections(**item_dict)
            self.session.add(insert_object)
        
    def packages(self, package_data):
        '''
        Serializes the elements of an API response containing package data and 
        inserts it into the database, based on the session 
        
        Parameters
        ----------
        package_data : JSON Object
            JSON resulting from a govInfo API call to the 
            '/collections/{endpointName}' URI, where endpointName is one of the 
            endpoints monitored.
            
        Returns
        -------
        None.
        '''
        self.logger.info("Writing to 'package' table")
        for item in package_data['packages']:
            self.logger.debug("Serializing item: %s"%item)
            item_dict = {
                'run_id' : self.run_id,
                'package_id' : item['packageId'],
                'last_modified': datetime.strptime(item['lastModified'], 
                                                   gpo_date_frmt),
                'package_link' : item['packageLink'],
                'doc_class' : item['docClass'],
                'title' : item['title'],
                }
            self.logger.debug('Inserting item: %s'%item_dict)
            insert_object = package(**item_dict)
            self.session.add(insert_object)
            
    def package_summaries(self, package_sum_data):
        '''
        Serializes the elements of an API response containing package summary 
        data and inserts it into the database, based on the session. 

        Parameters
        ----------
        package_sum_data : JSON Object
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        self.logger.info('Writing to package_summary table')
        for item in package_sum_data:
            self.logger.debug('Serializing item: %s' %item)
            item_dict = {
                'run_id' : self.run_id,
                'package_id' : item['packageId'],
                'title' : item['title'],
                'collection_code' : item['collectionCode'],
                'collection_name' : item['collectionName'],
                'category' : item['category'],
                'date_issued' : datetime.strptime(item['dateIssued'], 
                                                  '%Y-%m-%d'),
                'details_link' : item['detailsLink']
                    }
            self.logger.debug('Inserting item: %s'%item_dict)
            insert_object = packageSummary(**item_dict)
            self.session.add(insert_object)
    
    def committees(self, package_sum_data):
        '''
        Serializes the elements of an API response containing commttee data and 
        inserts it into the database, based on the session 

        Parameters
        ----------
        package_sum_data : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        self.logger.info('Writing to committees table')
        for item in package_sum_data:    
            for data in item['committees']:
                self.logger.debug('Serializing item: %s'%item)
                item_dict = {
                    'run_id' : self.run_id,
                    'package_id' : package_sum_data['packageId'],
                    'chamber' : item['chamber'],
                    'committee_type' : item['committeeType'],
                    'committee_name' : item['committeeName']
                    }
                self.logger.debug('Inserting item: %s'%item_dict)
                insert_object = committees(**item_dict)
                self.session.add(insert_object)
            
            
    def members(self, package_sum_data):
        '''
        Serializes the elements of an API response containing member data and 
        inserts it into the database, based on the session 

        Parameters
        ----------
        package_sum_data : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        self.logger.info('Writing to members table')
        for item in package_sum_data:    
            for data in item['members']:
                self.logger.debug('Serializing item: %s'%item)
                item_dict = {
                    'run_id' : self.run_id,
                    'package_id' : package_sum_data['packageId'],
                    'member_name' : item['memberName'],
                    'bioguide_id' : item['bioGuideId'],
                    'chamber' : item['chamber'],
                    'party' : item['party'],
                    'role' : item['role'],
                    'state' : item['state'],
                    'congress' : item['congress'],
                    'authority_id' : item['authorityId']
                    }
                self.logger.debug('Inserting item: %s'%item_dict)
                insert_object = members(**item_dict)
                self.session.add(insert_object)