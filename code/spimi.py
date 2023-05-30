from utils import *

class SPIMI:
    def __init__(self):
        self.inverted_index = defaultdict(list)
        self.block = 0
        # it's in kilobytes, when size is reached, writes the block
        self.BLOCK_SIZE = 10000

    def search_query(self, query, documents, top_k):
        # if index exists don't build another one
        if not os.path.isfile('../spimi_inverted_index.txt'):
            self.index_documents(documents)
        
        query_terms = preprocess({'text': query})

        self.inverted_index = generate_index()

        term_frequency = defaultdict(int)

        # ---- QUERY ----
        # Get term frecuency
        for term in query_terms:
            term_frequency[term] += 1

        weights = defaultdict(float)
        
        # ---- COSINE DISTANCE ----
        for term, frequency in term_frequency.items():
            # x -> tf = word frequency / amount of documents
            tf_idf = frequency/len(documents)

            # list with weight for each document
            weight_list = []
            
            # Similar to linked lists intersection algorithm
            index = 0
            # Gets term weight for each document
            for doc_id in range(get_n_docs()):
                if index != len(self.inverted_index[term]) and self.inverted_index[term][index][0] == doc_id:
                    weight_list.append(self.inverted_index[term][index])
                    index += 1
                else:
                    weight_list.append((doc_id, 0.0))

            # Sums the term weight to the document weight
            for doc_id in range(get_n_docs()):
                weights[doc_id] += weight_list[doc_id][1] * tf_idf
            
        # Sorts the dict by value to get the best scored documents first
        sorted_results = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        sorted_results = sorted_results[:int(top_k)]
        return sorted_results

    def index_documents(self, documents):
        for doc_id, document in enumerate(documents):       
            terms = preprocess(document)
            term_frequency = defaultdict(int)

            for term in terms:                              # Get frequency of each word
                term_frequency[term] += 1

            for term, frequency in term_frequency.items():
                if sys.getsizeof(self.inverted_index) > self.BLOCK_SIZE:
                    write_to_disk(self.inverted_index, f"../blocks/block-{self.block}.txt")
                    self.inverted_index.clear()
                    self.block += 1
                self.inverted_index[term].append((doc_id, frequency))
            
            term_frequency.clear()

        if self.inverted_index:                             # Write another block if inverted index isn't empty
            write_to_disk(self.inverted_index, f"../blocks/block-{self.block}.txt")
            self.inverted_index.clear()
                                                            # Apply merge sort
        merged_block = merge_all_blocks(get_files_from_folder("../blocks/"))
                                                            # Write main index
        write_to_disk_with_tfidf(merged_block, "../spimi_inverted_index.txt", 6)

        return