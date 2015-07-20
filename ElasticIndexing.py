from elasticsearch import Elasticsearch
import MongoEx
import pandas as pd

class ElasticIndexing:
    def __init__(self):
        self.es = Elasticsearch([{'host':'localhost','port':9200}])
        self.db = MongoEx.MongoEx().db
        self.ans = self.db['ans2014'].find_one()['topicanswer']
        self.coll = self.db['article']
        self.ans = self.db['ans2014'].find_one()['topicanswer']
        self.que = self.db['que2014'].find_one()['topic']

    def buildquery(self):
        filename = 'query2014.csv'
        data = pd.DataFrame()

        for entry in self.que:
            topic = entry['number']
            description = entry['description']
            summary = entry['summary']
            data = data.append(pd.DataFrame({"topic":[topic], "description" : [description],'summary':[summary]}))

        data.to_csv(filename,columns=['topic','description','summary'],index=False,sep='\t')

    def buildanswer(self):
        filename = 'answer2014.csv'
        data = pd.DataFrame()

        for entry in self.ans:
            pmcid = entry['pmcid']
            topic = entry['topicnum']
            relevancy = entry['FIELD4']
            data =data.append(pd.DataFrame({'pmcid':[pmcid],'topic':[topic],'relevancy':[relevancy]}))
        data.to_csv(filename,columns=['pmcid','topic','relevancy'],index=False,sep='\t')

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

