import re
import pandas as pd
from lxml import etree
query = "//e:full-text-retrieval-response/e:originalText/xocs:doc/xocs:serial-item/ja:article/ja:body/ce:sections/"
doi_query = "//e:full-text-retrieval-response/e:originalText/xocs:doc/xocs:meta/xocs:doi/text()"
csv_dict = {}
def path_extract(file_parser,error_path,paper_doi):
    paths = ['ce:section']
    pattern = re.compile(r"ce:section[[0-9]{2}]$")
    for e in file_parser.iter():
        path = file_parser.getpath(e)
        path_ = re.search(pattern, path)
        if path_:
            try:
                print(re.split('/\*/\*\[\d\]/ce:sections/',path))
                final_path = re.split('/\*/\*\[\d\]/ce:sections/',path)[1]
            except Exception as e:
                print(e)
                with open(error_path,'a') as fp:
                    print(paper_doi,file=fp)
                return None
            # if path_.group() == 'ce:section[1]':
            #     print(final_path)
            #     print(final_path[::-1].replace("ce:section[1]"[::-1],"ce:section"[::-1], 1)[::-1])
            #     print("*"*50)
            #     paths.append(final_path[::-1].replace("ce:section[1]"[::-1],"ce:section"[::-1], 1)[::-1])
            
            paths.append(final_path)
    return paths


# with open("test.json",'w', encoding="utf-8") as fp:
def text_extract(filepath ,doc,paper_doi,error_path):
    root = doc.getroot()
    # print(root)
    ns = root.nsmap.copy()
    ns["e"] = ns.pop(None)
    # print(ns)
    sections = root.xpath(query + f"ce:section/ce:section-title/text()", namespaces=ns)
    temp_dict = {}
    paths = path_extract(doc,paper_doi=paper_doi,error_path=error_path)
    if not paths:
        return
    paths.pop(0)
    # print(len(paths))
    temp = []
    for path in paths:
        paper_doi = ''.join(root.xpath(doi_query,namespaces = ns)).replace('/','_').replace('.','_')
        para_query  = query + path + f"/ce:para/text()"
        section_label_query = query + path + f"/ce:label/text()"
        section_label = root.xpath(section_label_query, namespaces=ns)
        section_title_query =  query + path + f"/ce:section-title/text()"
        section_title = ''.join(root.xpath(section_title_query, namespaces=ns))
        para = ''.join(root.xpath(para_query, namespaces=ns))
        para = para.strip('\n')
        para = para.strip('\t')
        temp.append(para)
        # if len(section_label):  
        #     if re.search('(\d(\.\d)+)', section_label[0]):
        #         print(section_label)
        #     else:
        #         temp_dict["title"] = f"{section_title}"
        #         temp_dict["text"] = f"{para}"

        # csv_dict.append(temp_dict)
        # temp_dict = {}
        # print(''.join(para),file=fp,end='\n\n')
    # json.dump(csv_dict, fp=fp,indent=4)
    csv_dict["text"] = temp 
    df = pd.DataFrame(csv_dict)
    # print(paper_doi)
    print("saving the file")
    df.to_csv(filepath)   

# doc_ = etree.parse('./test.xml')
# print(doc_)
# text_extract(1,doc_)