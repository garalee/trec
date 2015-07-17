import MongoEx
import ElasticIndexing
import ElasticSearching
import ElasticTraining

if __name__ == "__main__":
    training = ElasticTraining.ElasticTraining()
    indexing = ElasticIndexing.ElasticIndexing()
    searching = ElasticSearching.ElasticSearching()

    
    scheme = ['bm25','tfidf','ib','lmd','lmj']

    #indexing.doIndex()


    
    #training.test()
    # for ds in ['description','summary']:
    #     for i in range(1,31):
    #         training.buildVectorWithScheme(i,ds)

    for s in scheme:
        for ds in ['description','summary']:
            for i in range(1,31):
                training.buildVectorWithField(s,ds,i)


    
    # Field Training
    # print "Field Training..."
    # for ds in ['description','summary']:
    #     for s in scheme:
    #         for i in range(1,31):
    #             r.fieldweight_training(s,i,ds)
    # print "Field Training Done"


    
    # print "Scheme Training..."
    # # Scheme Training 
    # for i in range(1,31):
    #     for ds in ['description','summary']:
    #         r.schemeweight_training(i,ds)
    # print "Scheme Training Done"
