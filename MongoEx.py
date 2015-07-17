import sys
import pymongo
from pymongo import MongoClient


class MongoEx:
    HOST = "mongodb://202.30.23.40:27017"
    
    def __init__(self):
        self.client = pymongo.MongoClient(MongoEx.HOST)
        self.db = self.client['trec']

    def readAll(self,collection_name):
        collection = self.db[collection_name]
        for posts in collection.find():
            # print "Class:",posts['_class']
            # print "ID:",posts['_id']
            # print "PMCID:",posts['pmcid']
            # print "title:",posts['title']

            for key in posts['sectionList'][0]:
                print "Section List:",posts['sectionList'][0][key]
            
