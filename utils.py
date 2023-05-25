from collections import defaultdict
import math, os, sys
from nltk.stem.snowball import SnowballStemmer
import time

def get_n_block():
    path = "./blocks/"
    return len(os.listdir(path))

def preprocess(document):
    with open("stop_words_spanish.txt", "rt") as f:
        stoplist = {word.strip() for word in f}

    stemmer = SnowballStemmer('spanish')

    raw_words = document['text'].lower().split()
    words = []
    for word in raw_words:
        word = word.strip('?"º(),.')
        if word not in stoplist:
            word = stemmer.stem(word)
            words.append(word)
    return words

def write_to_disk(inverted_index, document_lengths, filename):

    #print(sys.getsizeof(inverted_index),"bytes!")
    #print(inverted_index,end="\n\n")

    with open(filename, 'w') as file:
        for term, postings in inverted_index.items():
            file.write(f"{term}: {postings}\n")
        file.write('\n')
        for doc_id, length in document_lengths.items():
            file.write(f"{doc_id}: {length}\n")

def generate_index():
    inverted_index = defaultdict(list)
    with open("spimi_inverted_index.txt", "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            
            term, doc_weights = line.split(' ', 1)
            doc_weights = doc_weights.split()

            for doc_w in doc_weights:
                doc_id, weight = doc_w.split(':')
                doc_id = int(doc_id)
                weight = float(weight)
                inverted_index[term].append((doc_id, weight))
    return inverted_index

def read_txt_files(folder_path):
    file_list = os.listdir(folder_path)
    data_list = []

    for i, file_name in enumerate(file_list):
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, 'r', encoding="utf-8") as file:
            text = file.read()

        data = {
            'id': int(i),
            'text': text
        }
        data_list.append(data)

    return data_list