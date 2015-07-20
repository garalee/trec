import numpy as np
import pandas as pd

class ElasticAnalyzer:
    def __init__(self):
        self.fieldData = pd.read_csv(open('analysis/field_result.csv'),sep='\t')
        self.schemeData = pd.read_csv(open('analysis/scheme_result.csv'),sep='\t')
        self.que = self.db['que2014'].find_one()['topic']
        self.ans = self.db['ans2014'].find_one()['topicanswer']
        self.scheme = ['bm25','tfidf','ib','lmd','lmj','dfr']
    
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

    
