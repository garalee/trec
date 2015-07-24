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

    def buildPairDB(self):
        filename1 = 'pair_answer2014.csv'
        filename2 = 'eval_answer2014.csv'
        
        tByTopic = []

        ans = pd.read_csv(open('answer2014.csv'),sep='\t')
        for i in range(1,31):
            tByTopic.append(ans[ans['topic'] == i])

        
        l = pd.DataFrame()
        eva = pd.DataFrame()

        cum =  0
        for topic_bundle in tByTopic:
            relnum = len(topic_bundle[(topic_bundle['relevancy']==2) | (topic_bundle['relevancy']==1)])
            cnt = (relnum*4)/5
            zerocnt = cnt
            cum = cum + cnt
            print "COUNT:",cnt
            print "CUM :", cum
            for idx,entry in topic_bundle.iterrows():
                if ((entry['relevancy'] == 1) or (entry['relevancy'] == 2)) and (not cnt == 0):
                    l = l.append(pd.DataFrame({
                                "pmcid" : [entry['pmcid']],
                                "topic" : [entry['topic']],
                                "relevancy" : [entry['relevancy']]
                                }))
                    cnt = cnt - 1
                elif (entry['relevancy'] == 0) and (not zerocnt == 0):
                    l = l.append(pd.DataFrame({
                                "pmcid" : [entry['pmcid']],
                                "topic" : [entry['topic']],
                                "relevancy" : [entry['relevancy']]
                                }))
                    zerocnt = zerocnt - 1
                else:
                    eva = eva.append(pd.DataFrame({
                                "pmcid" : [entry['pmcid']],
                                "topic" : [entry['topic']],
                                "relevancy" : [entry['relevancy']]
                                }))

        l.to_csv(filename1,sep='\t',index=False)
        eva.to_csv(filename2,sep='\t',index=False)

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
        pmcList = []
        relevancyList = []

        for index,entry in self.ans.iterrows():
            if entry['topic'] == num:
                pmcList.append(entry['pmcid'])
                relevancyList.append(entry['relevancy'])

        reTable = pd.DataFrame({"pmcid":pmcList,"relevancy":relevancyList})

        content = query[ds].replace(r"/",',')
        token = content.split(' ')
        content = [ x for idx,x in enumerate(token) if not idx == 0]
        content = ' '.join(content)

        analyzer = "my_"+scheme+"_analyzer"

        resTitle= self.es.search(index=scheme+"_garam",q='title:' + content,doc_type='article',analyzer=analyzer,size=40000,request_timeout=200)
        print "Done with title :",len(resTitle['hits']['hits'])
        l = pd.DataFrame()
        for entry in resTitle['hits']['hits']:
            if entry['_source']['topicnum'] == num:
                pmcid = entry['_source']['pmcid']
                score = entry['_score']
                l = l.append(pd.DataFrame({"pmcid":[pmcid], 'title':[score]}))

        resAbstract= self.es.search(index=scheme+"_garam",q='abstract:'+content,doc_type='article',analyzer=analyzer,size=40000,request_timeout=200)
        print "Done with abstract :",len(resAbstract['hits']['hits'])
        resBody= self.es.search(index=scheme+"_garam",q='body:'+content,doc_type='article',analyzer=analyzer,size=40000,request_timeout=200)
        print "Done with body :",len(resBody['hits']['hits'])
        

        v = l
        l = pd.DataFrame()
        
        for entry in resAbstract['hits']['hits']:
            if entry['_source']['topicnum'] == num:
                pmcid = entry['_source']['pmcid']
                score = entry['_score']
                l = l.append(pd.DataFrame({"pmcid":[pmcid], 'abstract' : [score]}))
        print "V:",len(v)
        print "L:",len(l)
    
        v = pd.merge(v,l,how='outer',on=['pmcid'])
        l = pd.DataFrame()
        for entry in resBody['hits']['hits']:
            if entry['_source']['topicnum'] == num:
                pmcid = entry['_source']['pmcid']
                score = entry['_score']
                l = l.append(pd.DataFrame({"pmcid":[pmcid], 'body' : [score]}))

        v = pd.merge(v,l,how='outer',on=['pmcid'])
        v=v.fillna(0)
        v = pd.merge(v,reTable,how='inner',on=['pmcid'])
        v=v.fillna(0)
        v.to_csv(filename,sep='\t',index=False)

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

        filename = "field" + "_" + scheme+"_" + ds + "_"  + str(num) + ".csv"
        filename_training = "field" + "_" + scheme+"_" + ds + "_"  + str(num) + "_training.csv"
        filename_eval = "field" + "_" + scheme+ "_" + ds + "_" + str(num) + "_eval.csv" 
        print "Working on",filename
        data = pd.read_csv(open("search_result/"+filename),sep='\t')

        training = pd.DataFrame()
        evaluation = pd.DataFrame()

        cnt = len(data[(data['relevancy'] == 1) | (data['relevancy'] == 2)])*4/5
        zero_cnt = cnt

        for idx,entry in data.iterrows():
            if entry['relevancy'] == 0:
                if zero_cnt == 0:
                    evaluation = evaluation.append(entry)
                else:
                    #training = training.append(entry)
                    zero_cnt = zero_cnt - 1
            else:
                if cnt == 0:
                    evaluation = evaluation.append(entry)
                else:
                    training = training.append(entry)
                    cnt = cnt - 1

        training.to_csv('vector/'+filename_training,sep='\t',index=False)
        evaluation.to_csv('vector/'+filename_eval,sep='\t',index=False)        
            
    def training_field(self,scheme,ds):
        l = pd.DataFrame()
        for i in range(1,24):
            print "Topic :",str(i)
            em_min = float("inf")
            remember_alpha = 0
            remember_beta = 0
            filename = 'field_' + scheme + '_' + ds + '_' + str(i) + '_training.csv'
            data = pd.read_csv(open("vector/"+filename),sep='\t')
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

                    if em.sum() < em_min:
                        em_min = em.sum()
                        remember_alaph = alpha
                        remember_beta = beta
            print "Alpha:",(1-remember_alpha)*(1-remember_beta)
            print "Beta:",(1-remember_alpha)*remember_beta
            print "Gamma:",remember_alpha

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
