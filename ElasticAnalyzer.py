import numpy as np
import pandas as pd

class ElasticAnalyzer:
    def __init__(self):
        self.es = Elasticsearch([{'host':'210,107,192,201','port':9200}])
        self.que = pd.read_csv(open('query2014.csv'),sep='\t')
        self.ans_eval = pd.read_csv(open('eval_answer2014.csv'),sep='\t')
        self.scheme = ['bm25','tfidf','ib','lmd','lmj','dfr']
    

    def query_field_control(self,scheme,ds,topic,num,weights):
        (alpha,beta,gamma) = weights
        for index,entry in self.que.iterrows():
            if entry['topic'] == topic:
                query =entry
                break
        
        
        content = query[ds].replace(r"/",',')
        token = content.split(' ')
        content = [x for idx,x in enumerat(toeken) if not idx ==0]
        content = ' '.join(content)
        analyzer = "my_" + scheme + "_analyzer"

        resTitle = self.es.search(index=scheme+"_garam_eval",q='title:'+content,doc_type='article',analyzer=analyzer,size=10000)
        resAbstract = self.es.search(index=scheme+"_garam_eval",q='abstract:'+content,doc_type='article',analyzer=analyzer,size=10000)
        resBody = self.es.search(index=scheme+"_garam_eval",q='body:'+content,doc_type='article',analyzer=analyzer,size=10000)

        for entry in resTitle['hits']['hits']:
            if entry['_source']['topicnum'] == 
            pmcid = entry['_id']
            score = entry['_score']
        

    def query_field_comparison(self,scheme,ds,topic):
        for index,entry in self.que.interrows():
            if entry['topic'] == topic:
                query = entry
                break

        content = query[ds].replace(r"/",',')
        token = content.split(' ')
        content = [x for idx,x in enumerat(toeken) if not idx ==0 ]
        content = ' '.join(content)
        analyzer = "my_" + scheme + "_analyzer"

        res = self.es.search(index=scheme+"_garam_eval",content,doc_type="article",analyzer = analyzer, size=10000)

        l = pd.DataFrame()
        for entry in res['hits']['hits']:
            if entry['_source']['topicnum'] == topic:
                pmcid = entry['_source']['pmcid']
                score = entry['score']
                relevancy = entry['_source']['relevancy']
                l = l.append(pd.DataFrame({"pmcid" : [pmcid],"score":[score], "relevancy":[relevancy]}))

        return l

    
    def runTestWithField(self,alpha,beta,gamma,scheme,ds):
        for i in range(1,31):
            
            for entry in self.ans:
                universe = pd.DataFrame()
                if entry['topicnum'] == i:
                    universe = universe.append({'pmcid' : entry['pmcid'],'relevancy' : entry['FIELD4']})
                    
            for entry in self.que:
                if entry['number'] == str(i):
                    query=entry

            content = query[ds].replace(r"/",',')
            analyzer = "my_"+scheme+"_analyzer"
            resTitle = self.es.search(index=scheme+"_garam_eval",doc_type="article",q="title:"+content,analyzer=analzyer,size=15000,request_time=120)
            resAbstract = self.es.search(index=scheme+"_garam_eval",doc_type="article",q="abstract:"+content,analyzer=analzyer,size=15000,request_time=120)
            resBody = self.es.search(index=scheme+"_garam_eval",doc_type="article",q="body:"+content,analyzer=analzyer,size=15000,request_time=120)

            res = self.es.search(index=scheme+"_garam_eval",doc_type="article",q=content,analyzer=analyzer,size=15000,request_time=120)

            titleScore = pd.DataFrame()
            abstractScore = pd.DataFrame()
            bodyScore = pd.DataFrame()
            comparison = pd.DataFrame()
            control = pd.DataFrame()

            
            for r in resTitle['hits']['hits']:
                pmcid = r['_source']['pmcid']
                if pmcid in universe['pmcid']:
                    score = r['_score']
                    titleScore = titleScore.append(pd.DataFrame({"pmcid" :[pmcid],"score":[score]}))
                                 
            for r in resAbstract['hits']['hits']:
                pmcid = r['_source']['pmcid']
                if pmcid in universe['pmcid']:
                    score = r['_score']
                    abstractScore = abstractScore.append(pd.DataFrame({"pmcid" :[pmcid],"score":[score]}))
            for r in resBody['hits']['hits']:
                pmcid = r['_source']['pmcid']
                if pmcid in universe['pmcid']:
                    score = r['_score']
                    bodyScore=bodyScore.append(pd.DataFrame({"pmcid" :[pmcid],"score":[score]}))
            
            for r in res['hits']['hits']:
                pmcid = r['_source']['pmcid']
                if pmcid in universe['pmcid']:
                    score = r['_score']
                    comparison=comparison.append(pd.DataFrame({"pmcid" : [pmcid],"score":[score]}))
            # Start to test
            for pmcid in universe['pmcid']:
                score = 0
                if pmcid in titleScore['pmcid']:
                    score = score + alpha*titleScore[titleScore['pmcid']== pmcid]['score']
                if pmcid in abstractScore['pmcid']:
                    score = score + beta*abstractScore[abstractScore['pmcid'] == pmcid]['score']
                if pmcid in bodyScore['pmcid']:
                    score = score + gamma*bodyScore[bodyScore['pmcid'] == pmcid]['score']

                control=control.append(pd.DataFrame({"pmcid" : pmcid,"score":score}))
                
            
                        
                    
                

    def runTestWithScheme(self,alpha,beta,ds):
        for i in range(1,31):
            for entry in self.ans:
                universe = pd.DataFrame()
                if entry['topicnum'] == i:
                    universe = universe.append({'pmcid' : entry['pmcid'],'relevancy' : entry['FIELD4']})
            for entry in self.que:
                if entry['number'] == str(i):
                    query=entry

            control=pd.DataFrame()
    
            for s1 in range(self.scheme):
                for s2 in range(s1+1,self.scheme):

                    content = query[ds].replace(r"/",',')
                    analyzer1 = "my_"+self.scheme[s1]+"_analyzer"
                    analyzer2 = "my_"+self.scheme[s2]+"_analyzer"

                    resA = self.es.search(index=self.scheme[s1]+"_garam_eval",doc_type="article",content,analyzer=analzyer1,size=15000,request_time=120)
                    resB = self.es.search(index=self.scheme[s2]+"_garam_eval",doc_type="article",content,analyzer=analzyer2,size=15000,request_time=120)

                    scoreA = pd.DataFrame()
                    scoreB = pd.DataFrame()
                    
                    for r in resA['hits']['hits']:
                        pmcid = r['_source']['pmcid']
                        if pmcid in universe['pmcid']:
                            score = r['_score']
                            scoreA = scoreA.append(pd.DataFrame({"pmcid":[pmcid],"score":[score]}))
                            
                    for r in resB['hits']['hits']:
                        pmcid = r['_source']['pmcid']
                        if pmcid in universe['pmcid']:
                            score = r['_score']
                            scoreB = scoreB.append(pd.DataFrame({"pmcid":[pmcid],"score":[score]}))
                                

                    for pmcid in universe['pmcid']:
                        score = 0
                        if pmcid in scoreA['pmcid']:
                            score = score + alpha*resA[resA['pmcid'] == pmcid]['score']
                        if pmcid in scoreB['pmcid']:
                            score = score + beta*resB[resB['pmcid'] == pmcid]['score']
                        contorl = control.append(pd.DataFrame({'pmcid':pmcid,'score':score})

                    
                        


    def field_display(self,num,ds):
        if ds == 's':
            term = 'summary'
        elif ds == 'd':
            term = 'description'
        else:
            return


        data = self.fieldData[self.fieldData['topic'] == num]

        print "<Weight Analysis>"
        print "topic:",str(num),term
        print "minimum loss :"
        print data.ix[data['loss'].argmin()]
        
    def scheme_display(self,num,ds):
        if ds == 's':
            term = 'summary'
        elif ds == 'd':
            term = 'description'
        else:
            return


        data = self.schemeData[self.schemeData['topic'] == num]

        print "<Weight Analysis>"
        print "topic:",str(num),term
        print "minimum loss :"
        print data.ix[data['loss'].argmin()]

    def scheme_showall(self):
        print self.schemeData

    def field_showall(self):
        print self.fieldData

    def scheme_getByTopic(self,num):
        print self.schemeData[self.schemeData['topic'] == num]

    def field_getByTopic(self,num):
        print self.fieldData[self.fieldData['topic'] ==num]

    def scheme_getByscheme(self,scheme):
        print self.schemeData[(self.schemeData['scheme1'] == scheme) | (self.schemeData['scheme2'] == scheme)]

    def field_getByscheme(self,scheme):
        print self.fieldData[self.fieldData['scheme'] == scheme]

    
