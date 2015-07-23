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



curl -XDELETE http://localhost:9200/$bm25
curl -XDELETE http://localhost:9200/${dfr}
curl -XDELETE http://localhost:9200/$ib
curl -XDELETE http://localhost:9200/$lmd
curl -XDELETE http://localhost:9200/$lmj
curl -XDELETE http://localhost:9200/$ngram
curl -XDELETE http://localhost:9200/$tfidf

