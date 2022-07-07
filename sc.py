import requests
import json
base_url_sc = "https://api.elsevier.com/content/search/sciencedirect"

headers = {
        'X-ELS-APIKey' : '45c6063a93408d8c4f3925dcf8e02e01',
        'Accept' : 'application/json'
}

data = {
        'qs': 'ALL ( "thermal adaptation" AND " behaviour" AND "buildings" AND "human" )',
       'offset': 0
       }

Url = "https://api.elsevier.com/content/search/sciencedirect"

r = requests.put(Url, data =json.dumps(data), headers=headers)
print(r.json())
# with open('science_put.json','w') as f:
#     json.dump(r.json(),indent=4,fp=f)