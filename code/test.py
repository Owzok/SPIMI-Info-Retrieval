import json
from collections import defaultdict
from utils import *
import sys
from operator import itemgetter
import linecache
import ast

def build_isam_index():
    interval = 500
    line_index = {}

    with open("../new_spimi_inverted_index.txt", "r") as input_file:
        with open("../new_isam_index.txt", "w") as index_file:
            byte_offset = 0
            line_number = 0

            while True:
                line = input_file.readline()
                if not line:
                    break

                if line_number % interval == 0:
                    index_file.write(f"{line.strip().split(':')[0]}:{byte_offset}\n")
                    line_index[line_number] = byte_offset

                byte_offset += len(line.encode())
                line_number += 1

    return line_index

def index_documents():
        documents_path = "../new_documents"
        inverted_index = defaultdict(list)
        BLOCK_SIZE = 30000
        block = 0
        amount_documents = 0
        """
        documents is a list of dict-like objects with a field for all the text in a document
        """
        documents = os.listdir(documents_path)
        for doc_name in documents:
            with open(documents_path + "/" + doc_name) as file:
                x = json.load(file)    
                for line in x:
                    doc_id = line['id']
                    amount_documents += 1
                    print(line['id'])
                    terms = preprocess(line)
                    term_frequency = defaultdict(int)

                    for term in terms:
                        term_frequency[term] += 1

                    for term, frecuency in term_frequency.items():
                        if sys.getsizeof(inverted_index) > BLOCK_SIZE:
                            sorted_blocks = sorted(inverted_index.items(), key=itemgetter(0))  # Sort blocks by term
                            write_to_disk(sorted_blocks, f"../new_blocks/block-{block}.txt")
                            inverted_index.clear()
                            block += 1
                        inverted_index[term].append((doc_id, frecuency))

                if inverted_index:                             # Write another block if inverted index isn't empty
                    sorted_blocks = sorted(inverted_index.items(), key=itemgetter(0))  # Sort blocks by term
                    write_to_disk(sorted_blocks, f"../blocks/block-{block}.txt")
                    inverted_index.clear()                      

        merged_block = merge_all_blocks(get_files_from_folder("../new_blocks/")) 
                                                            # Write main index
        write_to_disk_with_tfidf(merged_block, "../new_spimi_inverted_index.txt", amount_documents)
        build_isam_index()

#index_documents("../new_documents")
build_isam_index()