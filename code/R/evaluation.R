library(stringr)
setwd("C:\\Users\\ajou\\Documents\\TREC\\code\\Similarity_ranks")
getwd()
answers = read.csv("testDataAnswer.txt", sep = "\t")
head(answers)

for (i in 0:29 ) {
  assign(paste("answer", i+1, sep=''), answers[answers$topicNum==i,]['Pmcid'])
}

make_val <- function(path, name){
  for (i in 1:30 ) {
    col = c(path,i,".csv")
    file = paste(col, collapse = '')
    print(file)
    data = read.csv(file)
    #print(data)
    assign(paste(name, i, sep=''), data['pmcid'], envir = .GlobalEnv)
    print(paste(name, i, sep=''))
  }
  do_eval(name)
}

do_eval <- function(name){
  list <- vector()
  for (i in 1:30){
    data = paste(c(name, i), collapse = '')
    ans = paste(c("answer", i), collapse = '')
    print(ans[[1]])
    precision = paste(i, length(intersect(get(data)[[1]], get(ans)[[1]])), sep = ', ')
    print(paste(i, length(intersect(get(data)[[1]], get(ans)[[1]])), sep = ', '))  
  }
}


make_val(".\\TF-IDF(standard)\\description\\TF-IDF_description", "TF_IDF_description")
make_val(".\\TF-IDF(standard)\\summary\\TF-IDF_summary", "TF_IDF_summary")
make_val(".\\TF-IDF(5gram)\\description\\TF-IDF_5gram_description", "TF_IDF_5gram_description")
make_val(".\\TF-IDF(5gram)\\summary\\TF-IDF_5gram_summary", "TF_IDF_5gram_summary")
make_val(".\\BM25\\description\\BM25_description", "BM25_description")
make_val(".\\BM25\\summary\\BM25_summary", "BM25_summary")
make_val(".\\DFR\\descrption\\DFR_description", "DFR_description")
make_val(".\\DFR\\summary\\DFR_summary", "DFR_summary")
make_val(".\\IB\\description\\IB_description", "IB_description")
make_val(".\\IB\\summary\\IB_summary", "IB_summary")
make_val(".\\LMD\\description\\LMD_description", "LMD_description")
make_val(".\\LMD\\summary\\LMD_summary", "LMD_summary")
make_val(".\\LMJ\\description\\LMJ_description", "LMJ_description")
make_val(".\\LMJ\\summary\\LMJ_summary", "LMJ_summary")
