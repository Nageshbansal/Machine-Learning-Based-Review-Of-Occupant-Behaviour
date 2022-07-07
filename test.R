library(XML)
library(sys)


keyword_retrieve <- function(file){
  keywords <- c()
  doc = xmlTreeParse(file, useInternalNodes = TRUE)
  top = xmlRoot(doc)
  ack = names(top[[6]][["doc"]][["serial-item"]][["article"]][["head"]][["keywords"]])
  ack_xmls <- (xmlSApply(top[[6]][["doc"]][["serial-item"]][["article"]][["head"]][["keywords"]], xmlValue))
  
  for (i in ack_xmls){
    keyword <- i
    keywords <- append(keywords, keyword)
  }
  return(keywords)
}

files = list.files(path="~/Programming/Projects/elsevier-retrieve-papers/XML_Data", pattern=NULL, all.files=FALSE,
                   full.names=TRUE)
files
for (file in files){
  file
  keywords <- keyword_retrieve(file)
  print(keywords)
  keywords <- keywords[! keywords %in% c("Keywords")]
  write.table(keywords,file="~/Programming/Projects/elsevier-retrieve-papers/test.csv",append = TRUE,row.names = FALSE,col.names=FALSE)
  Sys.sleep(10)
}


