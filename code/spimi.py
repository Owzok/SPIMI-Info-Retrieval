from utils import *
import linecache
import ast

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

        #self.inverted_index = generate_index()

        term_frequency = defaultdict(int)

        # ---- QUERY ----
        # Get term frecuency
        for term in query_terms:
            term_frequency[term] += 1

        weights = defaultdict(float)
        
        # ---- COSINE DISTANCE ----
        with open("../spimi_inverted_index.txt") as index_file:
            for line in index_file.readlines():
                #get the term and counts for all 
                term = line.split(":")[0]

                # TODO:
                #todo esto es estupidiiiisimo por muchos motivos
                #1: estamos recorriendo el indice entero en cada query. Podriamos no hacerlo. este es el todo
                #2: estamos leyendo texto que se interpreta como codigo lo que es ESTUPIDO, y jamas deberia hacerse en produccion!!
                #3: procesar cosas con AST demora lo que demora compilar codigo: POR QUE CAR**O ESO ES ALGO QUE TENGO QUE HACER???
                #4: toda la ineficiencia esta en un bucle: pasar de un tipo de dato a otro, TODITO!!!

                # @Martin, has forzado mi mano a cometer sacrilegio. Odio todo

                if term in query_terms:
                    lista = ast.literal_eval("["+line.split(":")[1].strip()+"]")
                    for tf_idf in lista:
                        weights[tf_idf[0]] += term_frequency[term]*tf_idf[1];
        results = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        try:
            results = results[:int(top_k)]
        except:
            pass
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
                    write_to_disk(self.inverted_index, f"../blocks/block-{self.block}.txt")
                    self.inverted_index.clear()
                    self.block += 1
                self.inverted_index[term].append((doc_id, frequency))


        if self.inverted_index:                             # Write another block if inverted index isn't empty
            write_to_disk(self.inverted_index, f"../blocks/block-{self.block}.txt")
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
    
