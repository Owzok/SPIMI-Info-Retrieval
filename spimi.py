from utils import *

class SPIMI:
    def __init__(self):
        self.inverted_index = defaultdict(list)
        self.document_length = defaultdict(float)
        self.total_documents = 0
        self.document_frequency = defaultdict(int)
        self.block = 0
        self.blocks = []
        self.documents = []
        self.BLOCK_SIZE = 10000

    # freq: N word is repeated. doc_freq: in how many doc appears. Total: N of docs
    def calculate_tf_idf(self, frequency, document_frequency, total_documents):
        if document_frequency == 0:
            return 0

        tf = 1 + math.log10(frequency)
        idf = math.log10(1 + (total_documents / document_frequency))

        if idf == 0:
            print("\tFound ZERO:", total_documents, document_frequency)

        return tf * idf

    def merge(self):
        spimi_index = open('spimi_inverted_index.txt', 'a+', encoding='utf-8')

        for block in self.blocks:
            for term, postings in block.items():
                postings_str = ' '.join([f"{doc_id}:{tf_idf}" for doc_id, tf_idf in postings])
                
                spimi_index.write(f"{term} {postings_str}\n")
        
        spimi_index.close()

    def search_query(self, query, documents, top_k):
        if not os.path.isfile('spimi_inverted_index.txt'):
            print("Building index")
            self.index_documents(documents)
            
        self.documents = documents
        query_terms = preprocess({'text': query})

        inverted_index = generate_index()

        term_frequency = defaultdict(int)

        for term in query_terms:
            term_frequency[term] += 1

        # Calculate TF-IDF weights and update inverted index and document lengths
        weights = defaultdict(float)

        for term, frequency in term_frequency.items():
            #max_frequency = max(term_frequency.values())  # Calculate max frequency for the current term
            
            tf_idf = frequency/len(self.documents)
            x = tf_idf
            lst = []
            i = 0
            #print(inverted_index[term])
            for x in range(get_n_docs()):
                found = False
                if i != len(inverted_index[term]) and inverted_index[term][i][0] == x:
                    found = True
                    lst.append(inverted_index[term][i])
                    i += 1
                    #print("found", x, i, len(inverted_index[term]))
                    
                if not found:
                    lst.append((x, 0.0))
                    #print("not found", x, i, len(inverted_index[term]))

            for x in range(get_n_docs()):
                weights[x] += lst[x][1] * tf_idf
            
        sorted_results = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        sorted_results = sorted_results[:int(top_k)]
        return sorted_results

    def index_documents(self, documents):
        self.documents = documents
        self.total_documents = len(documents)

        for doc_id, document in enumerate(documents):       
            terms = preprocess(document)
            term_frequency = defaultdict(int)

            for term in terms:                              # Get frequency of each word
                term_frequency[term] += 1

            for term, frequency in term_frequency.items():
                if sys.getsizeof(self.inverted_index) > self.BLOCK_SIZE:
                    self.blocks.append(dict(self.inverted_index))
                    write_to_disk(self.inverted_index, f"./blocks/block-{self.block}.txt")
                    self.inverted_index.clear()
                    self.block += 1
                #tf_idf = self.calculate_tf_idf(frequency, self.document_frequency[term], self.total_documents)
                self.inverted_index[term].append((doc_id, frequency))
                #self.document_length[doc_id] += tf_idf ** 2
            
            term_frequency.clear()

            #for doc_id, length in self.document_length.items():
            #    self.document_length[doc_id] = math.sqrt(length)

        if self.inverted_index:                             # Write another block if inverted index isn't empty
            write_to_disk(self.inverted_index, f"./blocks/block-{self.block}.txt")
            self.blocks.append(dict(self.inverted_index))
            self.inverted_index.clear()
        
        merged_block = merge_all_blocks(get_files_from_folder("./blocks/"))
        write_to_disk_with_tfidf(merged_block, "spimi_inverted_index.txt", 6)

        #return self.document_length
        return