from elasticsearch import Elasticsearch
import numpy as np
import pandas as pd
import MongoEx

class ElasticTraining:
    def __init__(self):
        self.es = Elasticsearch([{'host':'localhost','port':9200}])
        self.db = MongoEx.MongoEx().db
        self.ans = self.db['ans2014'].find_one()['topicanswer']
        self.que = self.db['que2014'].find_one()['topic']
        self.field = ['title','body','abstract']
        self.scheme = ['tfidf', 'bm25','ib','lmd','lmj','dfr']

    def test(self):
         # Find the topic we are dealing with
        for entry in self.que:
            if entry['number'] == str(1):
                query = entry
                break

        content = query['description'].replace(r"/",",")
        res = self.es.search(index='tfidf',q=content,doc_type="article",analyzer="my_tfidf_analyzer",size=1500)

        print str(res['hits']['hits'][0]['_score'])
        
    def buildVectorWithScheme(self,num,description_summary):
        print "Building Scheme Score Vector..."
        filename = "scheme_score_vector_" + description_summary  +"_" +str(num)+".csv"
        # Find the topic we are dealing with
        for entry in self.que:
            if entry['number'] == str(num):
                query = entry
                break
                    
        pmcList = []
        relevancyList = []
    
        # pmcid and relevancy collecting
        for entry in self.ans:
            if entry['topicnum'] == num and (not entry['FIELD4'] == 0):
                pmcList.append(entry['pmcid'])
                relevancyList.append(entry['FIELD4'])

        print "Size(PMCLIST) : ",len(pmcList)
        
        v = pd.DataFrame({'pmcid' : pmcList,'relevancy' : relevancyList})
        
        
        content = query[description_summary].replace(r"/",",")
        for s in self.scheme:
            analyzer = "my_"+s+"_analyzer"
            res = self.es.search(index=s,q=content,doc_type="article",analyzer=analyzer,size=20000,request_timeout=30)

            print "HITS NUMBER:",str(len(res['hits']['hits']))
            l = []
            # score collecting
            for pmcid in pmcList:
                flag = False
                for entry in res['hits']['hits']:
                    if entry['_source']['pmcid'] == pmcid and entry['_source']['topicnum'] == num:
                        flag = True
                        l.append(entry['_score'])
                        break

                if not flag:
                    l.append(float(0))
                    
            temp = pd.DataFrame({ s : l})
            v = pd.concat([v,temp],axis=1)

        v.to_csv("vector/"+filename,index=False,sep=' ')
        return v
            
    def buildVectorWithField(self,scheme,description_summary,num):
        filename = "field_score_vector_" +scheme + "_" + description_summary + "_" + str(num) +".csv"
        for entry in self.que:
            if entry['number'] == str(num):
                query = entry
                break

        pmcList = []
        relevancyList = []

        for entry in self.ans:
            if entry['topicnum'] == num and (not entry['FIELD4'] == 0):
                pmcList.append(entry['pmcid'])
                relevancyList.append(entry['FIELD4'])
                
        v = pd.DataFrame({'pmcid' : pmcList, 'relevancy' : relevancyList})

        analyzer = "my_" + scheme + "_analyzer"
        content = query[description_summary].replace(r"/",',')
        resTitle = self.es.search(index=scheme,q="title:"+content,doc_type="article",analyzer=analyzer,size=10000)
        resAbstract = self.es.search(index=scheme,q="abstract:"+content,doc_type="article",analyzer=analyzer,size=10000)
        resBody = self.es.search(index=scheme,q="body"+content,doc_type="article",analyzer=analyzer,size=10000)

        titleList = []
        abstractList = []
        bodyList = []
        for pmcid in pmcList:
            flag = False
            for entry in resTitle['hits']['hits']:
                if entry['_source']['pmcid'] == pmcid and entry['_source']['topicnum'] == num:
                    flag = True
                    titleList.append(entry['_score'])
                    break

            if not flag:
                titleList.append(float(0))

            flag = False
            for entry in resAbstract['hits']['hits']:
                if entry['_source']['pmcid'] == pmcid and entry['_source']['topicnum'] == num:
                    flag = True
                    abstractList.append(entry['_score'])
                    break

            if not flag:
                abstractList.append(float(0))
                        
            flag = False
            for entry in resBody['hits']['hits']:
                if entry['_source']['pmcid'] == pmcid and entry['_source']['topicnum'] == num:
                    flag = True
                    bodyList.append(entry['_score'])
                    break
                
            if not flag:
                bodyList.append(float(0))
                        
        temp = pd.DataFrame({"title" : titleList, "body" : bodyList, "abstract" : abstractList})
        v = pd.concat([v,temp],axis=1)
        v.to_csv("vector/"+filename,index=False,sep=' ')
        
        return v
        

            
    def fieldweight_training(self,scheme,num,description_summary):
        
        em_min = float("inf")
        remember_alpha = 0

        filename = "field_training_"+str(num) + "_" + description_summary + "_" + scheme +".txt"
        t = open("analysis/" + filename,'w')
        for entry in self.que:
            if entry['number'] == str(num):
                query = entry

        for alpha in np.arange(0.1,1,0.01):
            empirical_loss =0
            beta = 1 - alpha

            analyzer = "my_" + scheme + "_analyzer"
            content = query[description_summary].replace(r"/",',')
            resTitle = self.es.search(index=scheme,q="title:"+content,doc_type="article",analyzer=analyzer,size=10000)
            resAbstract = self.es.search(index=scheme,q="abstract:"+content,doc_type="article",analyzer=analyzer,size=10000)
            resBody = self.es.search(index=scheme,q="body"+content,doc_type="article",analyzer=analyzer,size=10000)

            resTitle = sorted(resTitle['hits']['hits'],key = lambda A: A['_source']['pmcid'])
            resAbstract = sorted(resAbstract['hits']['hits'],key = lambda A: A['_source']['pmcid'])
            resBody = sorted(resBody['hits']['hits'],key = lambda A: A['_source']['pmcid'])


            if not (len(resTitle) == len(resAbstract) == len(resBody)):
                continue
            for idx in range(len(resTitle)):
                total = resTitle[idx]['_score'] + resAbstract[idx]['_score'] + resBody[idx]['_score']
                square = (1 - (resTitle[idx]['_score']*alpha/total + (resAbstract[idx]['_score'] + resBody[idx]['_score'])*beta/total))
                square = square * square
                empirical_loss = empirical_loss + square

            t.write("Empirical Loss:" + str(empirical_loss) + ": alpha :" + str(alpha) + '\n')
            if em_min > empirical_loss:
                em_min = empirical_loss
                remember_alpha = alpha
        t.write("Empirical Loss : "  + str(em_min) + " ,optimal alpha : " + str(remember_alpha))
        t.close()
                    

    def schemeweight_training(self,num,description_summary):
        em_min = float("inf")
        remember_alpha = 0

        filename = "scheme_training_"+str(num) + "_" + description_summary
    
        for entry in self.que:
            if entry['number'] == str(num):
                query = entry
                break
        
        for s1 in range(len(self.scheme)):
            for s2 in range(s1+1,len(self.scheme)):
                t = open("analysis/"+filename +self.scheme[s1]+"_"+self.scheme[s2]+'.txt','w')
                for alpha in np.arange(0.1,1,0.01):
                    empirical_loss = 0
                    beta = 1 - alpha
                    
                    analyzerA = "my_" + self.scheme[s1] + "_analyzer"
                    analyzerB = "my_" + self.scheme[s2] + "_analyzer"
                    content = query[description_summary].replace(r"/",',')
                    resA = self.es.search(index=self.scheme[s1],q=content,doc_type="article",analyzer=analyzerA,size=10000)
                    resB = self.es.search(index=self.scheme[s2],q=content,doc_type="article",analyzer=analyzerB,size=10000)
                        
                    resA = sorted(resA['hits']['hits'], key=lambda A: A['_source']['pmcid'])
                    resB = sorted(resB['hits']['hits'], key=lambda B: B['_source']['pmcid'])
                        
                    for idx,docA in enumerate(resA):
                        total = docA['_score'] + resB[idx]['_score']
                        square = (1 - (docA['_score']*alpha/total + resB[idx]['_score']*beta/total))
                        square = square*square
                        empirical_loss = empirical_loss + square

                    t.write("Empirical Loss:"+str(empirical_loss) + ": alpha :" + str(alpha) + '\n')
                    if em_min > empirical_loss:
                        em_min = empirical_loss
                        remember_alpha = alpha
                t.write("Empirical Loss : " + str(em_min) + ",optimal alpha:" + str(remember_alpha))
                t.close()
