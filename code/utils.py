from collections import defaultdict, OrderedDict    # for dicts
import math                                         # for log10
import os, sys                                      # for listdir and path
import json                                         # json.dump & .load
from nltk.stem.snowball import SnowballStemmer      # for stemmer
import re                                           # for regex in deleting special characters

def get_n_docs():
    return len(get_files_from_folder('../documents/'))

def preprocess(document):
    with open("../others/stop_words_spanish.txt", "rt") as f:
        stoplist = {word.strip() for word in f}

    stemmer = SnowballStemmer('spanish')

    raw_words = document['text'].lower().split()
    words = []
    for word in raw_words:
        word = re.sub(r'[^A-Za-z0-9]', '', word)  # Keep only A-Z and 0-9 characters
        if word and word not in stoplist:  # Check if the word is not empty after filtering
            word = stemmer.stem(word)
            words.append(word)
    return words


def calculate_tf_idf(frequency, document_frequency, total_documents):
    if document_frequency == 0:
        return 0

    tf = 1 + math.log10(frequency)
    idf = math.log10(1 + (total_documents / document_frequency))

    return tf * idf

def write_to_disk_with_tfidf(inverted_index, filename, total_documents):
    with open(filename, 'w') as file:
        for term, postings in inverted_index.items():
            document_frequency = len(postings)
            file.write(f"{term}: ")
            for posting in postings:
                document_id = posting[0]
                term_frequency = posting[1]
                tfidf = calculate_tf_idf(term_frequency, document_frequency, total_documents)
                file.write(f"[{document_id}, {tfidf}], ")
            file.write("\n")

def write_to_disk(inverted_index, filename):
    with open(filename, 'w') as file:
        json.dump(inverted_index, file, indent=4)

def generate_index():
    inverted_index = defaultdict(list)
    with open("../spimi_inverted_index.txt", "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            
            term, doc_weights = line.split(': ', 1)
            doc_weights = doc_weights.strip('[]').split('], [')
            
            for doc_w in doc_weights:
                doc_id, weight = doc_w.split(', ')
                doc_id = int(doc_id)
                weight = float(weight.split('],')[0])
                inverted_index[term].append([doc_id, weight])
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

def get_files_from_folder(folder_path):
    files = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            files.append(file_path)
    return files

def count_terms():
    count = 0
    with open("../spimi_inverted_index.txt", 'r') as file:
        for line in file:
            count += 1
    return count

# ----- MERGE ------

def merge_blocks(block1, block2):
    """
    Merge two blocks by merging the lists for duplicate words and sorting the postings
    """
    merged_block = OrderedDict()
    for block in [block1, block2]:
        for word, postings in block.items():
            if word in merged_block:
                merged_block[word] += postings
            else:
                merged_block[word] = postings

    sorted_block = OrderedDict()
    for word, postings in merged_block.items():
        sorted_postings = sorted(postings, key=lambda x: x[0])  # Sort the postings based on document ID
        sorted_block[word] = sorted_postings

    sorted_block = OrderedDict(sorted(sorted_block.items(), key=lambda x: x[0]))  # Sort the block by word

    return sorted_block

def merge_all_blocks(file_paths):
    """
    Merge all blocks from separate text files
    """
    blocks = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            block = json.load(file)  # Load the file content as a JSON object
            blocks.append(block)

    while len(blocks) > 1:
        merged_blocks = []
        for i in range(0, len(blocks), 2):
            if i + 1 < len(blocks):
                merged = merge_blocks(blocks[i], blocks[i + 1])
                merged_blocks.append(merged)
            else:
                merged_blocks.append(blocks[i])
        blocks = merged_blocks

    merged_result = blocks[0]
    sorted_result = OrderedDict(sorted(merged_result.items(), key=lambda x: x[0]))
    return sorted_result