import utils
import math
import json
from collections import OrderedDict

FILE_INDEX_SIZE = 1000

def index_files(isJson = False):
    '''
    Store the text contents of the files ordered by id
    expects the documents to be stored in a json file
    this subroutine does load all the corpus on main memory
    '''
    
    big_index = OrderedDict()

    for i in utils.get_files_from_folder('../documents'):
        with open(i) as file:
            loaded_file = json.load(file)
            big_index = big_index + {k['id']:k['text'] for k in loaded_file}
        print(big_index)

    # tengo el indice ordenado
    big_index.sort(key = lambda x: x['id'])
    big_index = [big_index[i:i + FILE_INDEX_SIZE] for i in range(0, len(big_index), FILE_INDEX_SIZE)] 
    
    with open('../indexed_docs/index.txt') as index_file:
        for i in big_index:

            




def getText(doc_id):
    '''
    retrieve the text content of the file based on its id
    '''

index_files()