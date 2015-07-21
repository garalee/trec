from elasticsearch import Elasticsearch
import numpy as np
import pandas as pd
import MongoEx

class ElasticTraining:
    def __init__(self):
        self.es = Elasticsearch([{'host':'localhost','port':9200}])
        self.que = pd.read_csv(open('query2014.csv'),sep='\t')
        self.ans = pd.read_csv(open('answer2014.csv'),sep='\t')
        self.field = ['title','body','abstract']
        self.scheme = ['tfidf', 'bm25','ib','lmd','lmj','dfr']

    def search_scheme(self,scheme,num,ds):
        filename = "search_result/"+ scheme + "_"+ds+"_"+str(num)+".csv"
        self.ans.sort(['topic','relevancy'],ascending=[1,0])

        for index,entry in self.que.iterrows():
            if entry['topic'] == num:
                query = entry
                break

        content = query[ds].replace(r"/",',')
        analyzer = "my_"+scheme+"_analyzer"
        res = self.es.search(index=scheme +"_garam",q=content,doc_type='article',analyzer=analyzer,size=5000,request_timeout=120)
        l = pd.DataFrame()
        for entry in res['hits']['hits']:
            pmcid = entry['_source']['pmcid']
            score = entry['_score']
            l = l.append(pd.DataFrame({"pmcid" : [pmcid],"score" : [score]}))

        l.to_csv(filename,sep='\t',index=False)

    def search_field(self,num,ds,scheme):
        filename = "search_result/"+"field_" + scheme + "_" +ds + "_" + str(num) + ".csv"
        for index,entry in self.que.iterrows():
            if entry['topic'] == num:
                query = entry
                break
            
        content = query[ds].replace(r"/",',')
        analyzer = "my_"+scheme+"_analyzer"
        v = pd.DataFrame()
        for t in ['title','abstract','body']:
            l = pd.DataFrame()
            
            res= self.es.search(index=scheme +"_garam",q= t+":"+content,doc_type='article',analyzer=analyzer,size=5000,request_timeout=120)
            
            for entry in res['hits']['hits']:
                pmcid = entry['_source']['pmcid']
                score = entry['_score']
                l = l.append(pd.DataFrame({t : [score]},index=[pmcid]))

            v = pd.concat([v,l],join='inner',axis=1)
        v.to_csv(filename,sep='\t')

    def training_scheme(self,filename):
        tokens = filename.split('_')
        topicnum = tokens[3].split('.')[0]
        ds = tokens[2]
        
        l = pd.DataFrame()
        data = pd.read_csv(open(filename),sep='\t')
        data['index'] = data.index
        data = data.rename(columns={'Unnamed: 0' : 'pmcid'})
        data.drop_duplicates(subset='pmcid',take_last=True,inplace=True)
        
        for s1 in range(len(self.scheme)):
            for s2 in range(s1+1,len(self.scheme)):
                min_em = float("inf")
                remember_alpha = 0
                for alpha in np.arange(0,1,0.01):
                    normA = data[self.scheme[s1]]/data[self.scheme[s1]].sum()
                    normB = data[self.scheme[s2]]/data[self.scheme[s2]].sum()
                        
                    score= alpha*normA + (1-alpha)*normB
                    relevancy = data['relevancy']

                    relevancy[relevancy == 1] = 0.75
                    relevancy[relevancy == 2] = 1

                    em = (relevancy - score) ** 2

                    if em.sum() < min_em:
                        min_em = em.sum()
                        remember_alpha = alpha
                                
                l = l.append(pd.DataFrame( 
                    {
                        'scheme1' : [self.scheme[s1]], 
                        'scheme2' : [self.scheme[s2]], 
                        'ds' : [ds], 
                        'topic' : [topicnum], 
                        'loss'  : [min_em], 
                        'alpha' : [remember_alpha],
                        'beta' : [1-remember_alpha]
                    }
                ))
        return l            
        
    def test(self):
         # Find the topic we are dealing with
        for entry in self.que:
            if entry['number'] == str(1):
                query = entry
                break

        content = query['description'].replace(r"/",",")
        res = self.es.search(index='tfidf',q=content,doc_type="article",analyzer="my_tfidf_analyzer",size=1500)

        print str(res['hits']['hits'][0]['_score'])

    def training_ds(self,filename):
        tokens = filename.split('_')
        scheme = tokens[3]
        num = tokens[4].split('.')[0]

        data = pd.read_csv(open(filename),sep='\t')

        em_min = float("inf")
        remember_alpha = 0
        for alpha in np.arange(0,1,0.01):
            normA = data['description']/data['description'].sum()
            normB = data['summary']/data['summary'].sum()

            score = alpha*normA + (1-alpha)*normB
            relevancy = data['relevancy']

            relevancy[relevancy == 1] = 0.5
            relevancy[relevancy == 2] = 1

            em = (relevancy - score) ** 2

            if em.sum() < em_min:
                em_min = em.sum()
                remember_alpha = alpha


        return pd.DataFrame(
            {
                'scheme' : [scheme],
                'topic' : [num],
                'loss' : [em_min],
                'alpha' : [remember_alpha]
                })

    def buildVectorWithDS(self,num,scheme):
        print "Building DS Score Vector...",scheme,":",str(num)
        filename = "DS_score_vector_" + scheme + "_" + str(num) + ".csv"

        for entry in self.que:
            if entry['number']== str(num):
                query = entry
                break

        pmcList = []
        relevancyList = []

        for entry in self.ans:
            if entry['topicnum'] == num:
                pmcList.append(entry['pmcid'])
                relevancyList.append(entry['FIELD4'])

        v = pd.DataFrame({'pmcid' : pmcList,'relevancy' : relevancyList})

        analyzer = "my_"+scheme+"_analyzer"

        
        content1 = query['summary'].replace(r"/",',')
        res1 = self.es.search(index=scheme + "_garam",q=content1,doc_type="article",analyzer=analyzer,size=10000)
        content2 = query['description'].replace(r"/",',')
        res2 = self.es.search(index=scheme + "_garam",q=content2,doc_type="article",analyzer=analyzer,size=10000)

        l1 = []
        l2 = []
        for pmcid in pmcList:
            flag = False
            for entry in res1['hits']['hits']:
                if entry['_source']['pmcid'] == pmcid:
                    flag=True
                    l1.append(entry['_score'])
                    break
            if not flag:
                l1.append(float(0))

            for entry in res2['hits']['hits']:
                if entry['_source']['pmcid'] == pmcid:
                    flag=True
                    l2.append(entry['_score'])
                    break
            if not flag:
                l2.append(float(0))

        temp1 = pd.DataFrame({ 'summary' : l1})
        temp2 = pd.DataFrame({ 'description' : l2})
        v = pd.concat([v,temp1,temp2],axis=1)
        v.to_csv("vector/"+filename,sep='\t')
        return v
                
                
        
    def buildVectorWithScheme(self,num,ds='summary'):
        v = pd.DataFrame()
        # Find the topic we are dealing with
       
        pmcList = []
        relevancyList = []
        
        # pmcid and relevancy collecting
        for index,entry in self.ans.iterrows():
            pmcList.append(entry['pmcid'])
            relevancyList.append(entry['relevancy'])

        for s in self.scheme:
            filename = s+ '_' + ds + '_' + str(num) + '.csv'
            print "Working on",filename
            data = pd.read_csv(open('search_result/'+filename),sep='\t')
            l = pd.DataFrame(columns=[s])

            for index,entry in data.iterrows():
                pmcid = entry['pmcid']
                score = entry['score']
                l = l.append(pd.DataFrame({s:[score]},index=[pmcid]))
            
            v = pd.concat([v,l],join='inner',axis=1)
        # merge schemes
        r = pd.DataFrame({'relevancy' : relevancyList},index=[pmcList])
        v = v.join(r,how='inner')
        # v = pd.concat([v,r],join='inner',axis=1)
        filename = 'scheme_vector_'+ ds + '_' + str(num) + '.csv'
        v.to_csv("vector/"+filename,sep='\t')
        return (v,r)
            
    def buildVectorWithField(self,scheme,num,ds='summary'):
        pmcList = []
        relevancyList = []

        for index,entry in self.ans.iterrows():
            pmcList.append(entry['pmcid'])
            relevancyList.append(entry['relevancy'])

            
        v = pd.DataFrame()

        for t in ['title','abstract','body']:
            filename = "search_result/"+"field" + "_" + scheme+"_" + ds + "_" + t + "_" + str(num) + ".csv"
            print "Working on",filename
            data = pd.read_csv(open(filename),sep='\t')
            l = pd.DataFrame(columns=[t])

            for index,entry in data.iterrows():
                pmcid = entry['pmcid']
                score = entry['score']
                l = l.append(pd.DataFrame({t:[score]},index=[pmcid]))
                    
            v = pd.concat([v,l],join='inner',axis=1)
            
        r = pd.DataFrame({'relevancy' : relevancyList},index=[pmcList])
        r = r.join(v,how='inner')
        r.to_csv('vector/'+filename,sep='\t')
        return r
            
    def training_field(self,scheme,ds):
        
        v = pd.DataFrame()
        for i in range(1,31):
            l = pd.DataFrame()
            em_min = float("inf")
            remember_alpha = 0
            remember_beta = 0
            filename = 'field_' + scheme + '_' + ds + '_' + str(i) + '.csv'
            data = pd.read_csv(open("search_result/"+filename),sep=',')
            data['index'] = data.index
            data = data.rename(columns={'Unnamed: 0' : 'pmcid'})
            data.drop_duplicates(subset='pmcid',take_last=True,inplace=True)
            
            for alpha in np.arange(0,1,0.01):
                for beta in np.arange(0,1,0.01):
                    normA = data['title']/data['title'].sum()
                    normB = data['abstract']/data['abstract'].sum()
                    normC = data['body']/data['body'].sum()

                score = (1-alpha)*(1-beta)*normA + (1-alpha)*beta*normB + alpha*normC
                relevancy = data['relevancy']

                relevancy[relevancy == 1] = 0.5
                relevancy[relevancy == 2] = 1

                em = (relevancy - score) ** 2

                #print "error :",em.sum(),"alpha :",alpha,",beta:",beta

                if em.sum() < em_min:
                    em_min = em.sum()
                    remember_alaph = alpha
                    remember_beta = beta

            l = l.append(pd.DataFrame({
                'scheme' : [scheme],
                'ds' : [ds],
                'topic' : [i],
                'loss' : [em_min],
                'alpha' : [(1-remember_alpha)*(1-remember_beta)],
                'beta' : [(1-remember_alpha)*remember_beta],
                'gamma' : [remember_alpha]
            }))
        l.to_csv('analysis/' +'field_' + scheme + '_' + ds+ '.csv',sep='\t',index=False)
