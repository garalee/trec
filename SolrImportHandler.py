import solr
import MongoEx


class SolrImportHandler:
    HOST = "http://localhost:8983/solr/trec_test"
    
    def __init__(self):
        self.connection = solr.Solr(SolrImportHandler.HOST)
        self.mongod = MongoEx.MongoEx()
        self.db = self.mongod.db

    def importAll(self,collection_name):
        collection = self.db[collection_name]
        cnt = collection.find().count()
        
        for i,posts in enumerate(collection.find()):
            _id = posts['_id']
            title = posts['title']
            pmcid = posts['pmcid']
            abstractList = posts['abstrctSectionList']
            abstract = ""
            for entry in abstractList:
                if 'paragraphs' in entry:
                    abstract = abstract + "\n" + entry['paragraphs']

            body = ""
            bodyList = posts['bodySectionList']
            for entry in bodyList:
                if 'paragraphs' in entry:
                    body = body + "\n" + entry['paragraphs']
            doc = {"_id" : _id,
                   "title" : title,
                   "pmcid" : pmcid,
                   "abstract" : abstract,
                   "body" : body,
            }
            
            self.connection.add(doc,commit=True)
            if i == cnt/100:
                break
            print str(i)+"/"+str(cnt/100)
