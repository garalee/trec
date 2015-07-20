import MongoEx
import ElasticIndexing
import ElasticSearching
import ElasticTraining
import pandas as pd
if __name__ == "__main__":
    training = ElasticTraining.ElasticTraining()    
    scheme = ['bm25','tfidf','ib','lmd','lmj']


    
    #training.test()
    # for ds in ['description','summary']:
    #     for i in range(1,31):
    #         training.buildVectorWithScheme(i,ds)

    # for s in scheme:
    #     for ds in ['description','summary']:
    #         for i in range(1,31):
    #             training.buildVectorWithField(s,ds,i)
                
    # print "\a"
    
    
    print "Scheme Training..."
    l = pd.DataFrame(columns=['scheme1','scheme2','ds','topic','loss','alpha'])
    for ds in ['description','summary']:
        for num in range(1,31):
            filename = "vector/scheme_score_vector_" + ds + "_" + str(num) + ".csv"
            l = l.append(training.training_scheme(filename))
    l.to_csv("analysis/scheme_result.csv",sep='\t',index=False,columns=['scheme1','scheme2','ds','topic','loss','alpha'])
    print "Done"
