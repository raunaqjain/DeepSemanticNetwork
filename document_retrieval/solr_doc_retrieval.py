import json
import pprint
import re
import urllib.request
from urllib.parse import quote

import en_core_web_sm
import unidecode

nlp = en_core_web_sm.load()

training_data = []
with open("shared_task_dev.jsonl", "r") as training_file:         #Mention the claim file for doc retrieval
    for line in training_file:
        training_data.append(json.loads(line))

# Setting up configuration for SOLR
NO_OF_DOC_TO_PICK = 5
core_name = "nlp"
no_of_rows = "20"
ip_address = "localhost:"
# ip_address = "3ef0a12c.ngrok.io"
HTTP = "http://"  # "https://"
port = "8984"
# port = ""
end_url = "/solr/" + core_name + "/select?"
main_url = HTTP + ip_address + port + end_url
FILE_PATH = 'document_retrieved_v4/ss_dev_v4_data'
IS_TEST_DATA = False      #TODO mark True for test doc only since they dont have label and verifiable


def create_query(query, doc=False):
    if doc:
        query_string = ""
        query_string += query[0]
        for i in range(1, len(query)):
            query_string += ' OR ' + query[i]
        return unidecode.unidecode(re.sub('"', '\\"', query_string))
        # return query_string
    else:
        query_string = ""
        query_string += query[0] + ' -LRB-.*?-RRB- '  # OR "' + query[0] + '"'
        for i in range(1, len(query)):
            query_string += ' OR ' + query[i] + ' -LRB-.*?-RRB-'  # ' OR "' + query[i] + '"'

        # return re.sub('"', '\\"', query_string)
        return unidecode.unidecode(query_string)


pp = pprint.PrettyPrinter(indent=4)
wiki_claims = []
file_count = 0  # TODO
for i, data in enumerate(training_data):
    print(i)
    claims = dict()
    claims['id'] = data['id']
    if not IS_TEST_DATA:
        claims['verifiable'] = data['verifiable']
        claims['label'] = data['label']
        claims['evidence'] = data['evidence']
    claims['claim'] = data['claim']
    claims['articles'] = dict()

    if not IS_TEST_DATA and data['verifiable'] == 'VERIFIABLE':
        evidence_articles = dict()
        for evidence_set in data['evidence']:
            for evidence in evidence_set:
                if evidence[2] not in evidence_articles:
                    evidence_articles[unidecode.unidecode(evidence[2])] = []
                evidence_articles[unidecode.unidecode(evidence[2])].append(evidence[3])

        query_list = list(evidence_articles.keys())
        query_string = create_query(query_list, True)
        # query_string = query_string.replace("_"," ")
        in_url = main_url + 'defType=edismax&fl=*,score&q=' + quote(
            query_string) + '&qf=id&stopwords=true&wt=json&indent=true&rows=' + no_of_rows

        # print(in_url)
        article_data = urllib.request.urlopen(in_url).read()
        docs = json.loads(article_data.decode('utf-8'))['response']['docs']
        if (len(docs) != len(evidence_articles)):
            print(in_url)
            print(data['claim'])
            print(evidence_articles.keys())
        for article in docs:
            temp = dict()
            temp['lines'] = article['lines']
            temp['id_string'] = article['id_string']
            temp['truth'] = True  # Meaning that it is the evidence document
            temp['predicted'] = False  # Initially False. If in predicted then changed to True
            temp['evidence_lines'] = evidence_articles[unidecode.unidecode(article['id'])]
            claims['articles'][article['id']] = temp
            # print(article['id'])

    #   PREDICT DOCUMENTS
    doc = nlp(data['claim'])
    query_list = [str(i) for i in doc.noun_chunks]
    if len(query_list) == 0:
        query_list = [data['claim']]
    #     print (query_list)
    query_string = create_query(query_list)
    query_string = query_string.replace("_", " ")
    in_url = main_url + 'defType=edismax&fl=*,score&pf=id_string&q=' + quote(
        query_string) + '&qf=id_string&stopwords=true&wt=json&indent=true&rows=' + no_of_rows
    # print(in_url)
    article_data = urllib.request.urlopen(in_url).read()
    docs = json.loads(article_data.decode('utf-8'))['response']['docs']

    count = 0
    for article in docs:
        try:
            if not IS_TEST_DATA and article['id'] in claims['articles'].keys():
                claims['articles'][article['id']]['predicted'] = True
                continue
            temp = dict()
            temp['lines'] = article['lines']
            temp['id_string'] = article['id_string']
            temp['truth'] = False  # Meaning that it is the evidence document
            temp['predicted'] = True  # If it is a predicted document
            temp['evidence_lines'] = []
            claims['articles'][article['id']] = temp
            count += 1
            if count == NO_OF_DOC_TO_PICK:
                break
        except Exception as e:
            continue
    # print(claims)
    wiki_claims.append(claims)
    if len(wiki_claims) % 10000 == 0:
        file_count += 1
        with open(FILE_PATH + str(file_count) + '.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(wiki_claims))
        wiki_claims.clear()

file_count += 1
with open(FILE_PATH + str(file_count) + '.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(wiki_claims))
