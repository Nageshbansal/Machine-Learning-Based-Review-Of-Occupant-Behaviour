
import requests
import pandas as pd
# import xml.etree.ElementTree as ET
from lxml import etree as ET
from urllib.error import HTTPError
from urllib.request import build_opener
from text_extractor import text_extract
# retrieve using scopus
base_url = "https://api.elsevier.com/content/search/scopus"
apiKey = "45c6063a93408d8c4f3925dcf8e02e01"
headers = {
    'X-ELS-APIKey': '45c6063a93408d8c4f3925dcf8e02e01',
    'Accept': 'application/json'
}
title = []
url = []

headers_xml = {
    'X-ELS-APIKey': '45c6063a93408d8c4f3925dcf8e02e01',
    'Accept': 'application/xml'
}

ns = {  
        'bk': 'http://www.elsevier.com/xml/bk/dtd', 
        'cals': 'http://www.elsevier.com/xml/common/cals/dtd', 
        'ce': 'http://www.elsevier.com/xml/common/dtd', 
        'ja': 'http://www.elsevier.com/xml/ja/dtd', 
        'mml': 'http://www.w3.org/1998/Math/MathML',
        'sa': 'http://www.elsevier.com/xml/common/struct-aff/dtd',
        'sb': 'http://www.elsevier.com/xml/common/struct-bib/dtd', 
        'tb': 'http://www.elsevier.com/xml/common/table/dtd', 
        'xlink': 'http://www.w3.org/1999/xlink', 'xocs': 'http://www.elsevier.com/xml/xocs/dtd', 
        'dc': 'http://purl.org/dc/elements/1.1/', 
        'dcterms': 'http://purl.org/dc/terms/', 
        'prism': 'http://prismstandard.org/namespaces/basic/2.0/', 
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 
        'e': 'http://www.elsevier.com/xml/svapi/article/dtd'
    }


def get_xml(paper_doi,error_path):
     
    url = "https://api.elsevier.com/content/article/doi/" + str(paper_doi) + "?apikey=" +headers_xml['X-ELS-APIKey'] +"&httpAccept=application/xml"
    try:
        print("Fetching the paper.....")
        opener = build_opener()
        response = opener.open(url)
        parsed = ET.parse(response)
        
        return parsed

    except Exception as e:
        print(e)
        with open(error_path,'a') as fp:
            print(paper_doi,file=fp)
        return None


# def get_doi(query, entry,j,start):  
    
#     count = 200
#     response = requests.get(
#         f'https://api.elsevier.com/content/search/scopus?query={query}&start={start}&count={count}',
#         headers=headers
#     )
#     response_json = response.json()
#     try:
#         doi = response_json['search-results']['entry'][entry]['prism:doi']
#     except:
#         with open('./OC_404_doi.txt', 'a') as f:
#             print(entry,file=f,flush=False)
#         return None    

#     # print(response_json)
#     print(doi)
#     return doi


def get_doi_csv(file_path):
    df = pd.read_csv("./scopus.csv",usecols=['DOI'])
    return df 


def retrieve_from_scopus():
    for j in range (0,100):
        start = 200 * j 
        for i in range(0, 200):   
            query = 'ALL("operational control" AND "thermal comfort" AND ("human" OR "building" OR "occupant"))'
            paper_doi = get_doi_csv(query, i,j,start)
            # y = scopus_paper_date(paper_doi)
            if paper_doi:
                get_xml(paper_doi)
            iter += 1
            print(iter)


def retriever(dst,src,error_path):
    paper_dois = get_doi_csv(src)
    iter = 1
    for doi in paper_dois["DOI"]:
        file_path = dst + str(iter)+ ".csv"
        print(file_path)
        parser = get_xml(doi,error_path)
        if parser:
            text_extract(file_path,parser,paper_doi=doi,error_path=error_path)
        iter += 1
        


get_xml("10.1016/j.scitotenv.2022.155128",'.')

if __name__ == "__main__":
    retriever("./testingcode/","scopus.csv","./testingcode/erros.txt")
