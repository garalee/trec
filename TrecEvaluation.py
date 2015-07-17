import MongoEx

# This class provides the functionality to evaluate the IR system we built
# The evaluation measure is "F-measure" because we cannot figure out whether
# the given document is relevant to the query.
#
# made by GR_factory 

class TrecEvaluation:
    def __init__(self):
        db = MongoEx.MongoEx().db
        answerTable = db['ans2014'].find_one()['topicanswer']
        questionTable = db['que2014'].find_one()['topic']
        

        self.answerSheet = [ [] for x in range(31)]
        for doc in answerTable:
            if not doc['FIELD4'] == 0:
                self.answerSheet[doc['topicnum']].append(doc['pmcid'])

        self.questionSheet = []
        for entry in questionTable:
            self.questionSheet.append(entry)

    # This function is helper function to evaluate the presion and recall
    def _evaluate(self,pmcList,topicnum):
        total_quess = len(pmcList)
        total_positive = len(self.answerSheet[topicnum])
        true_positive = 0
        
        for entry in pmcList:
            if entry in self.answerSheet[topicnum]:
                true_positive += 1

        precision = float(true_positive)/total_quess
        recall = float(true_positive)/total_positive

        return (precision,recall)
    # This function is main function to evaluate F-measure given the parameter 'beta'
    def Fmeasure(self,pmcList,topicnum,beta):
        (P,R) = self._evaluate(pmcList,topicnum)
        beta_sq = beta ** 2
        return (beta_sq+1)*P*R/(beta_sq*P + R)
        
    
