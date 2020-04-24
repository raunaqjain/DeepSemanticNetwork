import json
import os
import pprint
import urllib.request
from urllib.parse import quote

import en_core_web_sm

nlp = en_core_web_sm.load()

training_data = []
with open("train.jsonl", "r") as training_file:
    for line in training_file:
        training_data.append(json.loads(line))
        

# Setting up configuration for SOLR
core_name = "nlp"
no_of_rows = "20"
# ip_address = "localhost"
ip_address = "3ef0a12c.ngrok.io"
HTTP = "http://" #"https://"
# port = "8984"
port = ""
end_url = "/solr/" + core_name + "/select?"
main_url = HTTP + ip_address + port + end_url




def create_query(query, doc=False):
    if doc:
        query_string = ""
        query_string += query[0]
        for i in range(1, len(query)):
            query_string += ' OR ' + query[i]
        return "q=" + query_string
    else:
        query_string = ""
        query_string += query[0] + ' OR "' + query[0] + '"'
        for i in range(1, len(query)):
            query_string += ' OR ' + query[i] + ' OR "' + query[i] + '"'

        return "q="+query_string
    

    
pp = pprint.PrettyPrinter(indent=4)
wiki_claims = []
for data in training_data[:1]:
    claims = dict()
    claims['id'] = data['id']
    claims['verifiable'] = data['verifiable']
    claims['claim'] = data['claim']
    claims['label'] = data['label']
    
    evidence_articles = dict()
    for evidence_set in data['evidence']:
        for evidence in evidence_set:
            if evidence[2] not in evidence_articles:
                evidence_articles[evidence[2]] = []
            evidence_articles[evidence[2]].append(evidence[3])
                
    query_list = list(evidence_articles.keys())
    query_string = create_query(query_list, True)

    in_url = main_url + quote('defType=edismax&fl=*,score&'+query_string+'&qf=id&stopwords=true&wt=json&indent=true&rows='+no_of_rows,safe='&=', encoding=None, errors=None)
    article_data = urllib.request.urlopen(in_url).read()
    docs = json.loads(article_data.decode('utf-8'))['response']['docs']
    
    claims['articles'] = dict()
    for article in docs:
        temp = dict()
        temp['lines'] = article['lines']
        temp['id_string'] = article['id_string']
        temp['truth'] = True   #Meaning that it is the evidence document
        temp['predicted'] = False  #Initially False. If in predicted then changed to True
        temp['evidence_lines'] = evidence_articles[article['id']]
        claims['articles'][article['id']] = temp
        
    
#   PREDICT DOCUMENTS
    doc = nlp(data['claim'])
    query_list = [str(i) for i in doc.noun_chunks]
    if len(query_list) == 0:
        query_list = [data['claim']]
#     print (query_list)
    query_string = create_query(query_list)
    in_url = main_url + quote('defType=edismax&fl=*,score&pf=id_string&'+query_string+'&qf=id_string&stopwords=true&wt=json&indent=true&rows='+no_of_rows,safe='&=', encoding=None, errors=None)
    article_data = urllib.request.urlopen(in_url).read()
    docs = json.loads(article_data.decode('utf-8'))['response']['docs']
    
    
    count = 0
    for article in docs:
        try:
            if article['id'] in claims['articles'].keys():
                claim['articles'][article['id']]['predicted'] = True
                continue
            temp = dict()
            temp['lines'] = article['lines']
            temp['id_string'] = article['id_string']
            temp['truth'] = False   #Meaning that it is the evidence document
            temp['predicted'] = True  #If it is a predicted document
            temp['evidence_lines'] = []
            claims['articles'][article['id']] = temp
            count += 1
            if count == 4:
                break
        except Exception as e:
            continue
    wiki_claims.append(claims)
    if len(wiki_claims) % 10000 == 0:
        file_count += 1
        with open('document_retrieved/ss_training_data_temp'+str(file_count)+'.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(wiki_claims))
        wiki_claims.clear()
        
file_count += 1
with open('document_retrieved/ss_training_data_temp'+str(file_count)+'.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(wiki_claims))