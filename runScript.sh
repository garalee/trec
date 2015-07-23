# !/bin/bash

bm25="bm25";
dfr="dfr";
ib="ib";
lmd="lmd";
lmj="lmj";
tfidf="tfidf";
ngram="ngram";
host="http://localhost:9200";

bm25E="bm25_garam_eval"
dfrE="dfr_garam__eval"
ibE="ib_garam_eval"
lmdE="lmd_garam_eval"
lmjE="lmj_garam_eval"
tfidfE="tfidf_garam_eval"
ngramE="ngram_garam_eval"

curl -XPOST ${host}/$bm25/ -d @setting_BM25.json
curl -XPOST ${host}/$dfr/ -d @setting_DFR.json
curl -XPOST ${host}/$ib/ -d @setting_IB.json
curl -XPOST ${host}/$lmd/ -d @setting_LMD.json
curl -XPOST ${host}/$lmj/ -d @setting_LMJ.json
curl -XPOST ${host}/$tfidf/ -d @setting_TFIDF.json
curl -XPOST ${host}/$ngram/ -d @setting_NGRAM.json


curl -XPOST ${host}/$bm25E/ -d @setting_BM25.json
curl -XPOST ${host}/$dfrE/ -d @setting_DFR.json
curl -XPOST ${host}/$ibE/ -d @setting_IB.json
curl -XPOST ${host}/$lmdE/ -d @setting_LMD.json
curl -XPOST ${host}/$lmjE/ -d @setting_LMJ.json
curl -XPOST ${host}/$tfidfE/ -d @setting_TFIDF.json
curl -XPOST ${host}/$ngramE/ -d @setting_NGRAM.json
