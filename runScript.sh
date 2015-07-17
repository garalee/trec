# !/bin/bash

bm25="bm25";
dfr="dfr";
ib="ib";
lmd="lmd";
lmj="lmj";
tfidf="tfidf";
ngram="ngram";
host="http://localhost:9200";



curl -XPOST ${host}/$bm25/ -d @setting_BM25.json
curl -XPOST ${host}/$dfr/ -d @setting_DFR.json
curl -XPOST ${host}/$ib/ -d @setting_IB.json
curl -XPOST ${host}/$lmd/ -d @setting_LMD.json
curl -XPOST ${host}/$lmj/ -d @setting_LMJ.json
curl -XPOST ${host}/$tfidf/ -d @setting_TFIDF.json
curl -XPOST ${host}/$ngram/ -d @setting_NGRAM.json
