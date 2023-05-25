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
        tf = 1 + math.log10(frequency)
        idf = math.log10(1 + (total_documents / document_frequency))

        if idf == 0:
            print(total_documents, document_frequency)

        return tf * idf

    def merge(self):
        spimi_index = open('spimi_inverted_index.txt', 'a+')

        for block in self.blocks:
            for term, postings in block.items():
                postings_str = ' '.join([f"{doc_id}:{tf_idf}" for doc_id, tf_idf in postings])
                
                spimi_index.write(f"{term} {postings_str}\n")
        
        spimi_index.close()

    def search_query(self, query, documents):
        self.index_documents(documents)
        self.documents = documents
        query_terms = preprocess({'text': query})

        start_time = time.time()
        inverted_index = generate_index()
        line1_time = time.time()
        print(f"Index created in {line1_time - start_time}seconds")

        start_time = time.time()
        term_frequency = defaultdict(int)

        for term in query_terms:
            term_frequency[term] += 1

        # Calculate TF-IDF weights and update inverted index and document lengths
        weights = defaultdict(float)

        for term, frequency in term_frequency.items():
            #max_frequency = max(term_frequency.values())  # Calculate max frequency for the current term
            tf_idf = self.calculate_tf_idf(frequency, self.document_frequency[term], len(self.documents))
            x = tf_idf
            lst = []
            i = 0
            #print(inverted_index[term])
            for x in range(5):
                found = False
                if i != len(inverted_index[term]) and inverted_index[term][i][0] == x:
                    found = True
                    lst.append(inverted_index[term][i])
                    i += 1
                    #print("found", x, i, len(inverted_index[term]))
                    
                if not found:
                    lst.append((x, 0.0))
                    #print("not found", x, i, len(inverted_index[term]))

            for x in range(5):
                weights[x] += lst[x][1] * tf_idf
            
        sorted_results = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        line1_time = time.time()

        return sorted_results, (line1_time - start_time)

    def index_documents(self, documents):
        self.documents = documents
        self.total_documents = len(documents)

        for doc_id, document in enumerate(documents):       # Build document frequency dict O(dn)
            words = set(preprocess(document))
            for term in words:
                self.document_frequency[term] += 1

        for doc_id, document in enumerate(documents):       
            terms = preprocess(document)
            term_frequency = defaultdict(int)

            for term in terms:                              # Get frequency of each word
                term_frequency[term] += 1

            for term, frequency in term_frequency.items():
                if sys.getsizeof(self.inverted_index) > self.BLOCK_SIZE:
                    self.blocks.append(dict(self.inverted_index))
                    write_to_disk(self.inverted_index, self.document_length, f"./blocks/block-{self.block}.txt")
                    self.inverted_index.clear()
                    self.block += 1
                tf_idf = self.calculate_tf_idf(frequency, self.document_frequency[term], self.total_documents)
                self.inverted_index[term].append((doc_id, tf_idf))
                self.document_length[doc_id] += tf_idf ** 2
            
            term_frequency.clear()

            for doc_id, length in self.document_length.items():
                self.document_length[doc_id] = math.sqrt(length)

        if self.inverted_index:                             # Write another block if inverted index isn't empty
            write_to_disk(self.inverted_index, self.document_length, f"./blocks/block-{self.block}.txt")
            self.blocks.append(dict(self.inverted_index))
            self.inverted_index.clear()
            
        self.merge()

        return self.document_length