
import os
import pandas as pd
from lxml import etree as ET
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

download_papers = pd.DataFrame()
not_download_papers = pd.DataFrame()

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


def get_xml(paper_doi):
     
    url = "https://api.elsevier.com/content/article/doi/" + str(paper_doi) + "?apikey=" +headers_xml['X-ELS-APIKey'] +"&httpAccept=application/xml"
    try:
        opener = build_opener()
        response = opener.open(url)
        parsed = ET.parse(response)  
        return parsed

    except Exception as e:
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
    df = pd.read_csv(file_path)
    return df 


# def retrieve_from_scopus():
#     for j in range (0,100):
#         start = 200 * j 
#         for i in range(0, 200):   
#             query = 'ALL("operational control" AND "thermal comfort" AND ("human" OR "building" OR "occupant"))'
#             paper_doi = get_doi_csv(query, i,j,start)
#             # y = scopus_paper_date(paper_doi)
#             if not paper_doi:
#                 pass
#             else:
#                 get_xml(paper_doi)
#             iter += 1
#             print(iter)
iter =1
def retrieve_paper(paper, dst):
    global iter, not_download_papers, download_papers
    doi = paper[12]
    file_path = dst + str(iter)+ ".csv"
    parser = get_xml(doi)
    if not parser:
        not_download_papers = not_download_papers.append(paper, ignore_index=True)  
    else:
        p = text_extract(file_path,parser,paper_doi=doi)
        if not p:
            not_download_papers = not_download_papers.append(paper, ignore_index=True)
        else:
            download_papers = download_papers.append(paper, ignore_index=True)
     
    iter += 1
    

def retriever(savepath, src):
    papers_df = pd.read_csv(src)
    
    if not os.path.isdir(savepath):
        os.makedirs(savepath)

    files_to_save = os.path.join(savepath, "data/")
    if not os.path.isdir(files_to_save):    
        os.mkdir(files_to_save)

    meta_path = os.path.join(savepath, "metadata")
    os.mkdir(meta_path)
    papers_df.apply(lambda p : retrieve_paper(p, files_to_save),
                    axis=1,result_type='expand' )
    not_download_papers.to_csv(os.path.join(meta_path,'ndp.csv'), index=False)
    download_papers.to_csv(os.path.join(meta_path,'dp.csv'), index=False)

        




if __name__ == "__main__":
    # retriever(saving_path, dois_csv_path )
    retriever("./testingcode/","data/scopus.csv")
