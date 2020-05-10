# -*- coding: utf-8 -*-
"""
Created on Sun May  3 12:05:07 2020

@author: henry
"""

import sqlalchemy as db

engine = db.create_engine('sqlite:///../GPOWarehouse.sqlite')
metadata = db.MetaData()
connection = engine.connect()

#Global vars
run_stats = db.table('run_stats', metadata,
                       db.Column('run_id', db.Integer, primary_key=True),
                       db.Column('from_date', db.DateTime(), nullable=False),
                       db.Column('to_date', db.DateTime(), nullable=False),
                       db.Column('runtime', db.BigInteger, nullable=False),
                       )

#Overall Collection Stats
collections = db.Table('collections', metadata,
                       db.Column('collection_id',db.Integer,primary_key=True),
                       db.Column('run_id', db.Integer, 
                                 db.ForeignKey("run_stats.run_id"), 
                                 nullable = False),
                       db.Column('collection_code',db.String(100),nullable=False),
                       db.Column('collection_name',db.String(100),nullable=False),
                       db.Column('package_count',db.BigInteger,nullable=False),
                       db.Column('granule_count',db.BigInteger,nullable=True)
                       )

#Package overview
package = db.Table('package', metadata,
                    db.Column('package_id', db.Integer, primary_key=True),
                    db.Column('run_id', db.Integer, 
                                 db.ForeignKey("run_stats.run_id"), 
                                 nullable = False),
                    db.Column('collection_id', db.Integer, 
                              db.ForeignKey('collections.collection_id'),
                              nullable=False),
                    db.Column('package_type', db.String(10), nullable=False),
                    db.Column('package_name', db.String(100), nullable=False),
                    db.Column('package_link', db.String(100), nullable=False),
                    db.Column('doc_class', db.String(20), nullable = True),
                    db.Column('title', db.String(510), nullable = False),
                    db.Column('congress', db.Integer, nullable = True)
                    )

#Package details
package_detail = db.Table('package_detail', metadata,
                          db.Column('package_detail_id', db.Integer, 
                                    primary_key=True),
                          db.Column('run_id', db.Integer, 
                                 db.ForeignKey("run_stats.run_id"), 
                                 nullable = False),
                          db.Column('package_id', db.Integer, 
                                    db.ForeignKey("package.package_id"),
                                    nullable = False),
                          db.Column('category', db.String(50), nullable = True),
                          db.Column('date_issued'),
                          db.Column('branch', db.String(50), nullable = True),
                          db.Column('pages', db.Integer, nullable=True),
                          db.Column('government_author_one', db.String(50), nullable=True),
                          db.Column('government_author_two', db.String(50), nullable=True),
                          db.Column('bill_type', db.String(10), nullable=True),
                          db.Column('congress', db.Integer, nullable=True),
                          db.Column('origin_chamber', db.String(10), nullable=True), 
                          db.Column('current_chamber', db.String(10), nullable=True),
                          db.Column('session', db.Integer, nullable=True),
                          db.Column('bill_number', db.Integer, nullable=True),
                          db.Column('bill_version', db.String(5), nullable=True),
                          db.Column('is_appropriation', db.String(5), nullable=True),
                          db.Column('is_private', db.String(5), nullable=True),
                          db.Column('publisher', db.String(50), nullable=True),
                          
                          )

#Committees



#Members
members = db.Table('members', metadata,
                   db.Column('member_id', db.Integer, nullable=False, 
                             primary_key=True),
                   db.Column('run_id', db.Integer, 
                                 db.ForeignKey("run_stats.run_id"), 
                                 nullable = False),
                   db.Column('package_detail_id', db.Integer, 
                             db.ForeignKey('package_detail.package_detail_id'),
                             nullable=False),
                   db.Column('package_id', db.Integer, 
                                    db.ForeignKey("package.package_id"),
                                    nullable = False),
                   db.Column('bio_guide_id', db.String(10), nullable=False), 
                   db.Column('gpoId', db.Integer, nullable=False),
                   db.Column('chamber', db.String(1), nullable=False),
                   db.Column('party', db.String(1), nullable=False),
                   db.Column('role', db.String(10), nullable=False),
                   db.Column('state', db.String(2), nullable=False),
                   db.Column('congress', db.Integer, nullable=False),
                   db.Column('authority_id', db.Integer, nullable=False)
                   )

metadata.create_all(engine)