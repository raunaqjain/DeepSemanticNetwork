import ast
import json
import os
import unidecode

STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
    'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
    'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
    'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
    'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
    'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
    'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
    'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
    'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
    'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
    'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
    'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've',
    'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven',
    'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren',
    'won', 'wouldn', "'ll", "'re", "'ve", "n't", "'s", "'d", "'m", "''", "``"
}


def getFiles(path):
    for filename in os.listdir(path):
        yield filename

def processFiles(fileName):
    f = open(path + "/" + fileName, "r")
    f_write = open("/Users/anujbhargava7/Documents/ProcessedFiles/" + fileName.split(".")[0] + "_process.json", "w") #"/Users/anujbhargava7/Documents/Course/SEM2/NLP/Project/processed/" + fileName + "_process.json"
    fl = f.readlines()
    for x in fl:
        dict = ast.literal_eval(x)
        id = dict.get("id")
        if not bool(id.strip()):                            #Check if id is present or not
            continue
        id_without_underscore = dict.get("id").replace("_"," ")
        id_str = unidecode.unidecode(id_without_underscore)
        try:
            dict["id"] = unidecode.unidecode(id)  #TODO uncomment it for accent
        except Exception as e:
            dict["id"] = id
        try:
            dict["id_string"] = id_str
        except Exception as e:
            dict["id_string"] = id_without_underscore
        if "id" not in dict:
            print(dict.keys())
        dict["text_list"] = dict.get("text").split(".")
        print(json.dumps(dict), file=f_write)

if __name__ == "__main__":
    path = "/Users/anujbhargava7/Documents/Course/SEM2/NLP/Project/wiki"   #mention the path of the json file to processed
    for file in getFiles(path):
        if file.find("DS_Store") == -1:
            print(file)
            processFiles(file)
