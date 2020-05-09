import csv
import json
import random

# Load JSON data
total_count = 0
precision = 0
true_positive = 0
false_positive = 0
false_negative = 0
recall = 0
total_precision = 0
total_recall = 0
count = 1
claim_dict = dict()
total_verifiable_claims = 0
doc_claim_count = 0
total_doc_hits = 0
total_doc_claim_count = 0
while count <= 15:
    print("Count: ", count)
    # /Users/anujbhargava7/Documents/Projects/Pycharm-Workspace/NLP/document_retrieved_v2/ss_training_data1.json
    # /Users/anujbhargava7/Documents/Course/SEM2/NLP/Project/sentence_training_data/ss_training_data
    with open(
            '/Users/anujbhargava7/Documents/Projects/Pycharm-Workspace/NLP/document_retrieved_v2/ss_trainingv2_data' + str(
                count) + '.json') as json_file:
        data = json.loads(json_file.read())
    doc_claim_count = 0
    for entry in data:
        true_positive = 0
        false_positive = 0
        false_negative = 0
        if entry['verifiable'] == 'VERIFIABLE':
            total_verifiable_claims += 1
            doc_claim_count += 1
            total_doc_claim_count+=1
            if len(entry['articles']) > 0:
                total_evidences = len(entry['articles'])
                for evidence in list(entry['articles'].values()):
                    # print(evidence['truth'])
                    if evidence['truth'] and evidence['predicted']:
                        true_positive += 1
                        total_doc_hits += 1
                    if evidence['truth'] is False and evidence['predicted'] is True:
                        false_positive += 1
                    if evidence['truth'] is True and evidence['predicted'] is False:
                        false_negative += 1
                try:
                    precision = true_positive / (true_positive + false_positive)
                except ZeroDivisionError:
                    precision = 0
                try:
                    recall = true_positive / (true_positive + false_negative)
                except ZeroDivisionError:
                    recall = 0
            else:
                print("Id: ", entry['id'])
            total_precision += precision
            total_recall += recall
    count += 1
total_precision = total_precision / total_verifiable_claims
total_recall = total_recall / total_verifiable_claims
oracle_score = total_doc_hits / total_doc_claim_count
print("Precision is ", total_precision)
print("Recall is ", total_recall)
print("Total claims are ", total_verifiable_claims)
print("oracle score ", oracle_score)

# oracle_score = doc_id_hits / total
# with open('/Users/anujbhargava7/Documents/Projects/Pycharm-Workspace/NLP/document_retrieved_v2/ss_training_data15.json') as json_file:
#     data = json.loads(json_file.read())
#     print(len(data))
