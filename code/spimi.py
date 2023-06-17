from utils import *
import linecache
import ast
from operator import itemgetter

class SPIMI:
    def __init__(self):
        """ 
        inverted_index is a dictionary that looks like {term:[(doc1,freq1),(doc2,freq2)...]}. 
            Non existance of a (doc,freq) pair implies zero freq.
            It contains the last non-dumped section of the index
        """
        self.inverted_index = defaultdict(list) 
        self.block = 0
        # it's in kilobytes, when size is reached, writes the block
        self.BLOCK_SIZE = 30000
        self.interval = 500


    def search_query(self, query, documents, top_k):
        # if index exists don't build another one
        if not os.path.isfile('../spimi_inverted_index.txt'):
            print("[INFO] Creating Index. Hold on...")
            self.index_documents(documents)

        query_terms = preprocess({'text': query})

        term_frequency = defaultdict(int)
        weights = defaultdict(float)

        # ---- QUERY ----
        # Get term frequency
        for term in query_terms:
            term_frequency[term] += 1

        # ---- COSINE DISTANCE ----
        with open("../spimi_inverted_index.txt") as index_file:
            inverted_index = json.load(index_file)
            
        for term in query_terms:
            if term in inverted_index:
                postings = inverted_index[term]
                for posting in postings:
                    doc_id, tf_idf = posting.split(":")
                    weights[doc_id] += term_frequency[term] * float(tf_idf)

        results = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        results = results[:int(top_k)]

        return results

    def index_documents(self, documents):
        """
        documents is a list of dict-like objects with a field for all the text in a document
        """
        for doc_id, document in enumerate(documents):       
            terms = preprocess(document)           #terms is a list of all terms on this dicument
            term_frequency = defaultdict(int)

            for term in terms:                              # Get frequency of each word for this document
                term_frequency[term] += 1

            for term, frequency in term_frequency.items():
                if sys.getsizeof(self.inverted_index) > self.BLOCK_SIZE:
                    sorted_blocks = sorted(self.inverted_index.items(), key=itemgetter(0))  # Sort blocks by term
                    write_to_disk(sorted_blocks, f"../blocks/block-{self.block}.txt")
                    self.inverted_index.clear()
                    self.block += 1

                self.inverted_index[term].append((doc_id, frequency))

        if self.inverted_index:                             # Write another block if inverted index isn't empty
            sorted_blocks = sorted(self.inverted_index.items(), key=itemgetter(0))  # Sort blocks by term
            write_to_disk(sorted_blocks, f"../blocks/block-{self.block}.txt")
            self.inverted_index.clear()
                                                            # Apply merge sort
        #merged block is OrderedDict looking like {term:[(doc1,count1),(doc2,count2)...]}
        merged_block = merge_all_blocks(get_files_from_folder("../blocks/")) 
                                                            # Write main index
        write_to_disk_with_tfidf(merged_block, "../spimi_inverted_index.txt", 6)
        self.build_isam_index()
        return

    def build_isam_index(self):
        """
        When we open a file using the open() function in Python, the entire file is not loaded into RAM by default. 
        By default, file reading operations are buffered, which means that only a portion of the file (a buffer) 
        is loaded into memory at a time.

        When you read from the file using methods like read(), readline(), or iterate over the file object using a loop,
        the data is read from the buffer into memory. The size of the buffer used may vary depending on the platform and 
        the specific file object implementation.
        """
        line_index = {}

        with open("../spimi_inverted_index.txt", "r") as input_file:
            with open("../isam_index.txt", "w") as index_file:
                byte_offset = 0
                line_number = 0

                while True:
                    line = input_file.readline()
                    if not line:
                        break

                    if line_number % self.interval == 0:
                        index_file.write(f"{line.strip().split(':')[0]}:{byte_offset}\n")
                        line_index[line_number] = byte_offset

                    byte_offset += len(line.encode())
                    line_number += 1

        return line_index
    
