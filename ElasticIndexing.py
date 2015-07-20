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
        limit = 4*cnt/5
        # for i,posts in enumerate(self.ans):
        #     if limit < i:
        #         break
        #     pmcid = posts['pmcid']
        #     if self.coll.find({"articleMeta.pmcid" : str(pmcid)}).count() == 0:
        #         print "Data doesn't exist:",pmcid
        #         continue

        #     (title,abstract,body) = self.getDocument(pmcid)
                   
        #     docin = {"title" : title,
        #              "pmcid" : pmcid,
        #              "abstract" : abstract,
        #              "body" : body,
        #              "topicnum" : posts['topicnum'],
        #              "relevancy" : posts['FIELD4']
        #              }
            
        #     self.es.index(index="bm25_garam",doc_type="article",id=pmcid,body=docin)
        #     self.es.index(index="dfr_garam",doc_type="article",id=pmcid,body=docin)
        #     self.es.index(index="ib_garam",doc_type="article",id=pmcid,body=docin)
        #     self.es.index(index="lmd_garam",doc_type="article",id=pmcid,body=docin)
        #     self.es.index(index="lmj_garam",doc_type="article",id=pmcid,body=docin)
        #     self.es.index(index="tfidf_garam",doc_type="article",id=pmcid,body=docin)
        #     res = self.es.index(index="ngram_garam",doc_type="article",id=pmcid,body=docin)
        #     print res['created'],str(i)+"/"+str(cnt)
        
        for i,posts in enumerate(self.ans):
            if limit > i:
                continue

            pmcid = posts['pmcid']
            if self.coll.find({"articleMeta.pmcid" : str(pmcid)}).count() == 0:
                print "Data doesn't exist:",pmcid
                continue

            (title,abstract,body) =  self.getDocument(pmcid)

            docin={ "title" : title,
                    "pmcid" : pmcid,
                    "abstract" : abstract,
                    "body" : body,
                    "topicnum" : posts['topicnum'],
                    "relevancy" : posts['FIELD4']
                    }
            self.es.index(index="bm25_garam_eval",doc_type="article",id=pmcid,body=docin)
            self.es.index(index="dfr_garam_eval",doc_type="article",id=pmcid,body=docin)
            self.es.index(index="ib_garam_eval",doc_type="article",id=pmcid,body=docin)
            self.es.index(index="lmd_garam_eval",doc_type="article",id=pmcid,body=docin)
            self.es.index(index="lmj_garam_eval",doc_type="article",id=pmcid,body=docin)
            self.es.index(index="tfidf_garam_eval",doc_type="article",id=pmcid,body=docin)
            res = self.es.index(index="ngram_garam_eval",doc_type="article",id=pmcid,body=docin)
            print res['created'],str(i)+"/"+str(cnt)

