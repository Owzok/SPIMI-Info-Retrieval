from collections import defaultdict, OrderedDict    # for dicts
import math                                         # for log10
import os, sys                                      # for listdir and path
import json                                         # json.dump & .load
from nltk.stem.snowball import SnowballStemmer      # for stemmer
import re                                           # for regex in deleting special characters
import pickle
 
def get_n_docs():
    return len(get_files_from_folder('../documents/'))

def preprocess(document):
    """
    Takes a dict-like object with a field called text containing the entireity of text to be 
    preprocessed.
    Returns list of terms without special characters.

    TODO: Text must fit in ram to do this. Mabe readlinieify or specialize the function to deal with files?
    """
    with open("../others/stop_words_spanish.txt", "rt") as f:
        stoplist = {word.strip() for word in f}

    stemmer = SnowballStemmer('spanish')

    raw_words = document['text'].lower().split()
    words = []
    for word in raw_words:
        word = re.sub(r'[^A-Za-z]', '', word)  # Keep only A-Z and 0-9 characters
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

def calculate_idf(document_frequency,total_documents):
    return math.log10(1 + (total_documents / document_frequency))

def write_to_disk_with_tfidf(inverted_index, filename, total_documents):
    with open(filename, 'w') as file:
        for term, postings in inverted_index.items():
            document_frequency = len(postings)
            file.write(f"{term}:{calculate_idf(document_frequency, total_documents)}:")
            for posting in postings:
                document_id = posting[0]
                term_frequency = posting[1]
                tfidf = calculate_tf_idf(term_frequency, document_frequency, total_documents)
                file.write(f"{document_id},{tfidf}; ")
            file.write("\n")

def write_to_disk(inverted_index, filename):
    with open(filename, 'w') as file:
        json.dump(inverted_index, file, indent=4)

def read_txt_files(folder_path):
    #print("hi")
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
    # Count how many lines are on the index
    count = 0
    with open("../spimi_inverted_index.txt", 'r') as file:
        for line in file:
            count += 1
    return count

# ----- MERGE ------

"""
-- Ordered dict info

Time Complexity:
- Get item(Key): O(1)
- Set item(key, value): O(1)
- Delete item(key): O(n)
- Iteration: O(n)
- Space Complexity: O(n)

Ordered dict in Python version 2.7 consumes more memory than normal dict.
 This is due to the underlying Doubly Linked List implementation for keeping the order.
Starting from Python 3.7, insertion order of Python dictionaries is guaranteed.
"""

def merge_blocks(block1, block2):
    # Convert block1 and block2 to dictionaries
    block1_dict = dict(block1)
    block2_dict = dict(block2)

    # Merge two blocks by merging the dictionaries for duplicate words and sorting the postings
    merged_block = OrderedDict()
    for word, postings in block1_dict.items():
        if word in merged_block:
            merged_block[word] += postings
        else:
            merged_block[word] = postings

    for word, postings in block2_dict.items():
        if word in merged_block:
            merged_block[word] += postings
        else:
            merged_block[word] = postings

    sorted_block = OrderedDict(sorted(merged_block.items(), key=lambda x: x[0]))  # Sort the block by word

    return sorted_block

def merge_all_blocks(file_paths):
    # Merge all blocks from separate text files
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