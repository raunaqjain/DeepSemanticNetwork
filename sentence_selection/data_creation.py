import pandas as pd
import unicodedata
from tqdm import tqdm
import os
import random
from utils import parse_text, lines_to_items
import argparse


def parseRow(index, iid, verifiable, claim, label, article):
    data = []
    article_title = article['id_string']
    article_text = article['lines'][0]
    article_evidence = set(article['evidence_lines'])
    
    text = "\n" + unicodedata.normalize('NFD', article_text)
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
            
        if not temp['label'] and random.random() <= 1 - sample_prob:
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


def create_training_data(docs):
    training_data = []
    for i, doc in tqdm(enumerate(docs)):
        if ".json" not in doc:
            continue
        file_path = input_folder + "/" + doc
        print (file_path)
        df = pd.read_json(file_path)
    #     df = sentence_data.set_index(['id', "verifiable", "claim", "label"])['articles'].apply(pd.Series)
    #     df = df.stack().reset_index(name='articles').drop(['level_4'], axis = 1)
        for key, row in df.iterrows():
            iid, verifiable, claim, label, articles = row
            for article in articles:
                data = parseRow(key, iid, verifiable, claim, label, row['articles'][article])
                training_data.extend(data)
        print (i, doc)
    pd.DataFrame(training_data).to_csv(output_folder, index=False)
    print ("DATA SAVED")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Formulate data for sentence model")
    parser.add_argument("--input", help="path to input folder")
    parser.add_argument("--output", help="path to output file")
    parser.add_argument("--sample_prob", help="probability of choosing false labels", type=float, default=1.0)
    args = parser.parse_args()

    input_folder = args.input
    output_folder = args.output
    sample_prob = args.sample_prob
    print(sample_prob)
    # DOC_PATH = "doc_retrieval/document_retrieved_v2/"
    # SENTENCE_PATH = "sentence_training_data/v2/"

    list_of_docs = sorted(os.listdir(input_folder))
    print(list_of_docs)
    create_training_data(list_of_docs)


