from elasticsearch import Elasticsearch
import MongoEx

class ElasticIndexing:
    def __init__(self):
        self.es = Elasticsearch([{'host':'localhost','port':9200}])
        self.db = MongoEx.MongoEx().db
        self.ans = self.db['ans2014'].find_one()['topicanswer']
        self.coll = self.db['article']

    def getDocument(self,pmcid):
        res = self.coll.find({"articleMeta.pmcid" : str(pmcid)}).next()

        meta = res['articleMeta']
        content = res['articleContent']


        # title
        title = meta['title']
        # abstract
        abstract = ""
        if 'sectionList' in meta['abstractText']:
            for entry in meta['abstractText']['sectionList']:
                if 'paragraphs' in entry:
                    abstract = abstract + '\n' + entry['paragraphs']

        # body
        body = ""
        for entry in content['sectionList']:
            if 'paragraphs' in entry:
                body = body + '\n' + entry['paragraphs']
        
        return (title,abstract,body)
        


    def doIndex(self):
        cnt = len(self.ans)
        for i,posts in enumerate(self.ans):
            pmcid = posts['pmcid']
            if self.coll.find({"articleMeta.pmcid" : str(pmcid)}).count() == 0:
                continue
            (title,abstract,body) = self.getDocument(pmcid)

                   
            docin = {"title" : title,
                     "pmcid" : pmcid,
                     "abstract" : abstract,
                     "body" : body,
                     "topicnum" : posts['topicnum'],
                     "relevancy" : posts['FIELD4']
            }
            
            self.es.index(index="bm25",doc_type="article",id=pmcid,body=docin)
            self.es.index(index="dfr",doc_type="article",id=pmcid,body=docin)
            self.es.index(index="ib",doc_type="article",id=pmcid,body=docin)
            self.es.index(index="lmd",doc_type="article",id=pmcid,body=docin)
            self.es.index(index="lmj",doc_type="article",id=pmcid,body=docin)
            self.es.index(index="tfidf",doc_type="article",id=pmcid,body=docin)
            res = self.es.index(index="ngram",doc_type="article",id=pmcid,body=docin)
            print res['created'],str(i)+"/"+str(cnt)
            
