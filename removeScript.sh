# !/bin/bash

curl -XDELETE 'http://localhost:9200/bm25'
curl -XDELETE 'http://localhost:9200/dfr'
curl -XDELETE 'http://localhost:9200/ib'
curl -XDELETE 'http://localhost:9200/lmd'
curl -XDELETE 'http://localhost:9200/lmj'
curl -XDELETE 'http://localhost:9200/ngram'
curl -XDELETE 'http://localhost:9200/tfidf'
