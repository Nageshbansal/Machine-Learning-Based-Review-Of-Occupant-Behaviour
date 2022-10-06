library(XML)
library(sys)

file = "~/Programming/Projects/elsevier-retrieve-papers/XML_Data/10.1016-j.jobe.2022.104514.xml"
section <- c()
doc = xmlTreeParse(file, useInternalNodes = TRUE)
top = xmlRoot(doc)
names(top[["originalText"]][["doc"]][["serial-item"]][["article"]][["body"]][["sections"]][["section"]][["section-title"]])
ack = names(top[["originalText"]][["doc"]][["serial-item"]][["article"]][["body"]][["sections"]])
ack_xmls <- (xmlSApply(top[["originalText"]][["doc"]][["serial-item"]][["article"]][["body"]][["sections"]][["section"]][["section-title"]], xmlValue))

for (i in ack_xmls){
  print(i)
}



