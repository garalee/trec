import solr
from urllib2 import *
import simplejson


class QueryHandler:
    def query(self,term):
        conn = urlopen('http://localhost:8983/solr/trec_test/tvrh?tv.tf=true&tv.df=true&q=body:'+ term + '&indent=true&lf=pmcid&wt=json')
        rsp = simplejson.load(conn)
        return rsp

    def buildQueryVector(self,query):
        urlopen(
