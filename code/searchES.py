
# coding: utf-8

# In[2]:

from elasticsearch import Elasticsearch
es = Elasticsearch([{'host':'localhost', 'port':9200}])


# In[5]:

#res = es.index(index="trec25gram", doc_type='25gram', id=pmcid, body=data)  
#print(res['created'])
#res = es.get(index="trec", doc_type='articleSmall', id=pmcid)
#print(res['_source'])
query = {"title":"Lawrence"}
res = es.search(index="trec",doc_type="articleSmall", q="Lawrence")


# In[17]:

count = 0
for doc in res['hits']['hits']:
    count += 1
    print '{0}, {1}'.format(count,doc['_source']['pmcid'])


# In[ ]:



