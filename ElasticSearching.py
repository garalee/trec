from elasticsearch import Elasticsearch
import MongoEx
import csv

class ElasticSearching:
    def __init__(self):
        self.es = Elasticsearch([{'host':'localhost','port':9200}])
        self.db = MongoEx.MongoEx().db
        self.coll = self.db['ArticleSmallData2']

    def test(self):
        with open('summary2.csv','rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for idx,item in enumerate(reader):
                query = item['summary'].replace(r"/",',')
                abstractQuery = {"abstract" : query}
                res = self.es.search(index="trec",doc_type="BM25",q=query,analyzer="my_BM25_analyzer",size=100)
                for doc in res['hits']['hits']:
                    text = '{0},{1}'.format(doc['_source']['pmcid'],doc['_score'])
                    print text
