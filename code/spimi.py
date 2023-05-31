from utils import *
import linecache
import ast

class SPIMI:
    def __init__(self):
        self.inverted_index = defaultdict(list)
        self.block = 0
        # it's in kilobytes, when size is reached, writes the block
        self.BLOCK_SIZE = 30000
        self.interval = 500

    def search_query(self, query, documents, top_k):
        # if index exists don't build another one
        if not os.path.isfile('../spimi_inverted_index.txt'):
            self.index_documents(documents)
        
        query_terms = preprocess({'text': query})

        #self.inverted_index = generate_index()

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
                self.isam_binary_search(term)
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

    
    def isam_binary_search(self, word):
        with open("../isam_index.txt", "r") as file:
            lines = file.read().strip().split('\n')

        interval = int(lines[0])
        values = lines[1:]

        # Perform binary search
        left = 0
        right = len(values) - 1
        closest_word = None

        while left <= right:
            mid = (left + right) // 2
            current_word = values[mid]

            if current_word.lower() == word.lower():
                # Exact match found
                closest_word = current_word
                break
            elif current_word.lower() < word.lower():
                # Update closest_word and search in the right half
                closest_word = current_word
                left = mid + 1
            else:
                # Search in the left half
                right = mid - 1

        print("Closest word:", closest_word)

    def isam_binary_search(self, word):
        with open("../isam_index.txt", "r") as file:
            lines = file.read().strip().split('\n')

        values = lines[0:]

        # Perform binary search
        left = 0
        right = len(values) - 1
        closest_word = None

        while left <= right:
            mid = (left + right) // 2
            current_word = values[mid]

            if current_word.lower() == word.lower():
                # Exact match found
                closest_word = current_word
                break
            elif current_word.lower() < word.lower():
                # Update closest_word and search in the right half
                closest_word = current_word
                left = mid + 1
            else:
                # Search in the left half
                right = mid - 1

        self.read_index(int(closest_word.split(":")[1]))
        return

    def read_index(self, pos):
        self.inverted_index.clear()
        with open("../spimi_inverted_index.txt", "r") as file:
            file.seek(pos)
            
            lines = []
            for _ in range(self.interval+1):
                line = file.readline().strip()
                if not line:
                    break
                x = line.split(":")
                self.inverted_index[x[0]] = ast.literal_eval(x[1].strip("'"))
        return