answer = read.csv('testDataAnswer.txt', sep = '\t')
xmlfile <- xmlTreeParse('topics2014.xml')
xmltop = xmlRoot(xmlfile)
print(xmltop)[1:2]
plantcat <- xmlSApply(xmltop, function(x) xmlSApply(x, xmlValue))
plantcat_df <- data.frame(t(plantcat), row.names=NULL)
description <- plantcat_df[1:30,][1]
summary <- plantcat_df[1:30,][2]

write.table(description, file="description2.csv", sep = '')
write.table(summary, file="summary2.csv", sep = '')
