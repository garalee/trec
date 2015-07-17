import MongoEx
import solr
class BooleanRetrievalTraining:
    # Article Fields(pmcid, title, abstract, body)
    #
    def __init__(self):
        self.db = MongoEx.MongoEx().db
        self.ans_coll = self.db['ans2014'].find_one()['topicanswer']
        self.que_coll = self.db['que2014'].find_one()['topic']
        self.connection = solr.Solr('http://localhost:8983/solr/trec_test')
        self.alpha = 0.33       # title weighting
        self.beta = 0.33        # abstract weighting
        self.gamma = 1 - self.alpha - self.beta

    def selectByField(self,fieldname,value):
        return self.connection(str(fieldname + ":" + value))


    def getPMCFromAnswer(self,topicnum):
        pmcs = []
        for entry in self.ans_coll:
            if entry['topicnum'] == topicnum:
                pmcs.append(entry['pmcid'])
        return pmcs


    # This function calculates the score of the given document with respect to the query
    # Lemmization, or stemming is not taken into consideration.
    def calculateScore(self,document,query):
        score = 0
        for token in query.split(' '):
            if token in document['title']:
                score += self.alpha
            if token in document['abstract']:
                score += self.beta
            if token in document['body']:
                score += self.gamma
        
    
    # Intersection Method
    def query(self,topic):
        
        topic['description']
        topic['summary']

        for token in topic['description'].split(' '):
            pass
            
