import MongoEx
import ElasticIndexing
import ElasticSearching
import ElasticTraining
import pandas as pd
if __name__ == "__main__":
    training = ElasticTraining.ElasticTraining()
    #indexing = ElasticIndexing.ElasticIndexing()
    #searching = ElasticSearching.ElasticSearching()

    
    scheme = ['bm25','tfidf','ib','lmd','lmj','dfr']
    #indexing.doIndex()

    # print "Build DS Vector.."
    # for s in scheme:
    #     for i in range(1,31):
    #         print "<"+s+">" +"NUM : " + str(i)
    #         training.buildVectorWithDS(i,s)
    # print "\a"

    # print "Training DS Vector.."
    # l = pd.DataFrame(columns=['scheme','topic','loss','alpha'])
    # for s in scheme:
    #     for i in range(1,31):
    #         filename = "vector/DS_score_vector_"+s+"_" + str(i) + ".csv"
    #         l = l.append(training.training_ds(filename))
    # l.to_csv("analysis/ds_result.csv",sep='\t',index=False,columns=['scheme','topic','loss','alpha'])
    # print "Done"
    for s in scheme:
        for i in range(26,31):
            print s,i
            training.search(s,i,'summary')





    
    # print "Building Scheme Vector..."     
    # for ds in ['description','summary']:
    #     for i in range(1,31):
    #         training.buildVectorWithScheme(i,ds)
    # print "Scheme Vector Integration"
    # prefix = "scheme_score_vector"
    # training.buildVectorWithoutTN(prefix,'description')
    # training.buildVectorWithoutTN(prefix,'summary')

    # print "Scheme Training..."
    # l = pd.DataFrame(columns=['scheme1','scheme2','scheme3','ds','topic','loss','alpha','beta'])
    # for ds in ['description','summary']:
    #     for num in range(1,31):
    #         filename = "vector/scheme_score_vector_" + ds + "_" + str(num) + ".csv"
    #         l = l.append(training.training_scheme(filename))
    # l.to_csv("analysis/scheme_result.csv",sep='\t',index=False,columns=['scheme1','scheme2','scheme3','ds','topic','loss','alpha','beta'])
    # print "Done"


    # print "Building Field Vector..."
    # for s in scheme:
    #     for ds in ['description','summary']:
    #         for i in range(1,31):
    #             training.buildVectorWithField(s,ds,i)
    # print "Field Training....."
    # l = pd.DataFrame(columns=['scheme','ds','topic','loss','alpha','beta','gamma'])
    # for s in scheme:
    #     for ds in ['description','summary']:
    #         for num in range(1,31):
    #             filename = "vector/field_score_vector_" + s + "_" + ds + "_" + str(num) + ".csv"
    #             print filename
    #             print l
    #             l = l.append(training.training_field(filename))

    # l.to_csv("analysis/field_result.csv",sep='\t',columns=['scheme','ds','topic','loss','alpha','beta','gamma'],index=False)
    # print "Done"
