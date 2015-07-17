import MongoEx
import SolrImportHandler


if __name__ == "__main__":
    s = SolrImportHandler.SolrImportHandler()
    s.importAll('articleAbstractExist')
