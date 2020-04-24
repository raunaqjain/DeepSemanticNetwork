import pandas as pd
import unicodedata
from tqdm import tqdm
import os
import json
import random


def parse_text(data):
    lines = []
    i = 0
    while True:
        start = f'\n{i}\t'
        end = f'\n{i + 1}\t'
        start_index = data.find(start)
        end_index = data.find(end)
#         print (start_index, end_index)
#         print ("lines", data[start_index: end_index])
        if end_index == -1:
            extra = f'\n{i + 2}\t'
            extra_1 = f'\n{i + 3}\t'
            extra_2 = f'\n{i + 4}\t'

            # print(lines_b[start_index:])
            lines.append(data[start_index:])
            # print('What?')
            # print(lines_b)
            # print(extra, extra_1)
            # print(lines_b.find(extra))
            # print(lines_b.find(extra_1))
            # print(not (lines_b.find(extra) == -1 and lines_b.find(extra_1) == -1))

            if not (data.find(extra) == -1
                    and data.find(extra_1) == -1
                    and data.find(extra_2) == -1):
                print(data)
                print(extra, extra_1)
                print('Error')
            break

        lines.append(data[start_index:end_index])
        i += 1
    return lines



def lines_to_items(page_id, lines):
    lines_list = []

    for i, line in enumerate(lines):
        line_item = dict()

        line_item_list = line.split('\t')

        line_num = line_item_list[0]
        if not line_num.isdigit():
            print("None digit")
            print(page_id)

            print(lines)
            print(k)
        else:
            line_num = int(line_num)

        if int(line_num) != i:
            print("Line num mismath")
            print(int(line_num), i)
            print(page_id)

            print(k)

        line_item['line_num'] = line_num
        line_item['sentences'] = ''
        line_item['h_links'] = []

        if len(line_item_list) <= 1:
            lines_list.append(line_item)
            continue

        sent = line_item_list[1].strip()
        h_links = line_item_list[2:]

        if 'thumb' in h_links:
            h_links = []
        else:
            h_links = list(filter(lambda x: len(x) > 0, h_links))

        line_item['sentences'] = sent
        line_item['h_links'] = h_links
        # print(line_num, sent)
        # print(len(h_links))
        # print(sent)
        # assert sent[-1] == '.'

        if len(h_links) % 2 != 0:
            print(page_id)
            for w in lines:
                print(w)
            print("Term mod 2 != 0")

            print("List:", line_item_list)
            print(line_num, sent)
            print(h_links)
            print()

        lines_list.append(line_item)
    return lines_list


DOC_PATH = "doc_retrieval/document_retrieved_v2/"
SENTENCE_PATH = "sentence_training_data/v2/"

list_of_docs = sorted(os.listdir(DOC_PATH))


def create_training_data(index, iid, verifiable, claim, label, article):
    data = []
    article_title = article['id_string']
    article_text = article['lines'][0]
    article_evidence = set(article['evidence_lines'])
    
    
    text = "\n"+ unicodedata.normalize('NFD', article_text)
    lines = parse_text(text)
    lines = [line.strip().replace('\n', '') for line in lines]
    if len(lines) == 1 and lines[0] == '':
        lines = ['0']
    lines = lines_to_items(index, lines)
    for line in lines:
        if len(line['sentences'].split()) < 4:
            continue
        temp = dict()
        if line['line_num'] in article_evidence:
            temp['label'] = True
        else:
            temp['label'] = False
            
        if not temp['label'] and random.random() <= 0.6:
            continue
            
        temp['sentence'] = line['sentences']
        temp['id'] = iid
        temp['verifiable'] = verifiable
        temp['claim'] = claim
        temp['h_links'] = line['h_links']
        
        temp['claim_label'] = label
        temp['article_title'] = article_title
        data.append(temp)
    return data


training_data = []
for i, doc in tqdm(enumerate(list_of_docs)):
    if ".json" not in doc:
        continue
    file_path = DOC_PATH + doc
    df = pd.read_json(file_path)
#     df = sentence_data.set_index(['id', "verifiable", "claim", "label"])['articles'].apply(pd.Series)
#     df = df.stack().reset_index(name='articles').drop(['level_4'], axis = 1)    
    for key, row in df.iterrows():
#         import pdb; pdb.set_trace()
        iid, verifiable, claim, label, articles = row
        for article in articles:
            data = create_training_data(key, iid, verifiable, claim, label, row['articles'][article])
            training_data.extend(data)
    print (i, doc)
pd.DataFrame(training_data).to_csv(SENTENCE_PATH + "data.csv", index=False)
print ("DATA SAVED")
#     with open(SENTENCE_PATH + doc, "w") as f:
#         json.dump(training_data, f)

# d = pd.read_csv(SENTENCE_PATH + "data15.csv")