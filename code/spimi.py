from utils import *
import linecache
import ast
from operator import itemgetter

ZERO_TRESHOLD = 0.000001

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
        self.amount_documents = 0

    def search_query(self, query, top_k):
        # if index exists don't build another one
        if not os.path.isfile('../spimi_inverted_index.txt'):
            print("[INFO] Creating Index. Hold on...")
            self.index_documents()

        query_terms = preprocess({'text': query})

        term_frequency = defaultdict(int)
        weights = defaultdict(float)

        # ---- QUERY ----
        # Get term frequency
        for term in query_terms:
            term_frequency[term] += 1

        
        # ---- COSINE DISTANCE ---- | Scoring

        query_pow2_len = 0 
        docs_pow2_lens = defaultdict(float)
        
        with open("../spimi_inverted_index.txt") as index_file:
            for line in index_file.readlines():
                term, idf, wlist = self.processIndexLine(line)

                query_tf_idf = math.log10(1+term_frequency[term])*idf #tf_idf query
                query_pow2_len += query_tf_idf**2 #for normalization purposes. It is valid to ignore all terms 
                                                 # in the query that are not in the corpus because their idf would be zero
                for i in wlist:
                    #if query_tf_idf != 0:
                        #print(term)
                    docs_pow2_lens[i[0]] += i[1]**2 #for normalization purposes
                    weights[i[0]] += i[1]*query_tf_idf #dot product itself

        for i in weights:
            #to cull weird values introduced via ieee 774 errors
            if (query_pow2_len > ZERO_TRESHOLD and weights[i] > ZERO_TRESHOLD and weights[i] > ZERO_TRESHOLD):
                weights[i] = weights[i]/(math.sqrt(docs_pow2_lens[i])*math.sqrt(query_pow2_len))

        results = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        if top_k == "":
            top_k = "5"
        results = results[:int(top_k)]

        return results

    def processIndexLine(self,line):
        splitted = line.split(":")

        term = splitted[0]
        idf =  float(splitted[1])
        
        term_tfidf_list_str = splitted[2].split(';')[:-1]
        term_tf_idf_list = []
        for i in term_tfidf_list_str:
            term_tf_idf_list.append((int(i.split(',')[0]),float(i.split(',')[1])))
        return term, idf, term_tf_idf_list
        
    def index_documents(self):
            """
            documents is a list of dict-like objects with a field for all the text in a document
            """
            documents_path = "../documents"
            documents = os.listdir(documents_path)
            for doc_name in documents:
                with open(documents_path + "/" + doc_name) as file:
                    x = json.load(file)    
                    for line in x:
                        doc_id = line['id']
                        self.amount_documents += 1
                        #print(line['id'])
                        terms = preprocess(line)
                        term_frequency = defaultdict(int)

                        for term in terms:
                            term_frequency[term] += 1

                        for term, frecuency in term_frequency.items():
                            if sys.getsizeof(self.inverted_index) > self.BLOCK_SIZE:
                                sorted_blocks = sorted(self.inverted_index.items(), key=itemgetter(0))  # Sort blocks by term
                                write_to_disk(sorted_blocks, f"../blocks/block-{self.block}.txt")
                                self.inverted_index.clear()
                                self.block += 1
                            self.inverted_index[term].append((doc_id, frecuency))

                    if self.inverted_index:                             # Write another block if inverted index isn't empty
                        sorted_blocks = sorted(self.inverted_index.items(), key=itemgetter(0))  # Sort blocks by term
                        write_to_disk(sorted_blocks, f"../blocks/block-{self.block}.txt")
                        self.inverted_index.clear()                      

            merged_block = merge_all_blocks(get_files_from_folder("../blocks/")) 
                                                                # Write main index
            write_to_disk_with_tfidf(merged_block, "../spimi_inverted_index.txt", self.amount_documents)
            self.build_isam_index()

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
    
