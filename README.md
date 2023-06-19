<br>
<p align="center">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Circle-icons-rocket.svg/1200px-Circle-icons-rocket.svg.png" alt='Logo' width=80 height=80>

<h3 align="center">SPIMI Search Engine</h3>

<p align="center">
    Single-Pass In-Memory Indexing for information search and recovery
</p>

#
<p align="center"

![ga](https://img.shields.io/badge/Python-3.6-blue?style=for-the-badge&logo=)
![si](https://img.shields.io/badge/Academical%20Project-Yes-brightgreen?style=for-the-badge&logo=) 
![si](https://img.shields.io/badge/License-MIT-red?style=for-the-badge&logo=)
![si](https://img.shields.io/badge/Repo%20Size-2.8Mb-orange?style=for-the-badge&logo=)
<p align="center"

The **SPIMI** *(Single-Pass In-Memory Indexing)* project is a simple implementation of an indexing algorithm used in information retrieval systems. This project aims to demonstrate the basic concepts of building an inverted index using the SPIMI algorithm as well as comparing query search times from our python index against SQL indexation.
</p>

## Features
- Building an inverted index from a collection of documents.
- Support for tokenization, stop word removal, and stemming.
- Indexation for search optimization.
- Visual Interface.
- We have merged multiple stoplists over the internet to make the best one possible.
- Querying the inverted index to retrieve relevant documents.
- Searches in both Postgres and our system.

### Prerequisites

To run the SPIMI index project, you need to have the following installed:
- Python (version 3.6 or higher)
- NLTK (Natural Language Toolkit) library
- Pygame (SDL wrapped library)
- Psycopg2 (Python to SQL connection)

### Installation

1. Clone the repository to your local machine:
```shell
git clone https://github.com/your-username/spimi-index-project.git
```

2. Install the required dependencies:
```sh
pip install -r requirements.txt
```

## Documents
The documents to be indexed are tweets collected from 07-08-2018 to 03-05-2018 provided to us by our instructor. The data was cleaned by reducing it to a collection of JSON files containing lists of structures of the form document text ("text") field and an id ("id") field. In total there are around 133 thousand entries in this dataset.


## Usage
1. Prepare your collection of documents in a suitable format (e.g., JSON files containing structures of the form {"id":id, "text": text-body}) and put them into the documents folder.

2. Update the ```main.py``` file with the appropriate configuration parameters and paths to your document collection.

3. Create an empty database in your postgreSQL and fill in line 13 in ```gui.py```:
   ```pg_querier = PG("<your-db-name>","<your-user>","<your-user-password>")```

4. Change the directory to the main location:

```sh
cd 'code'
```

5. Run the ```main.py``` script to run the program:

```sh
python main.py
```

6. After attempting the first search, the index is built automatically using the documents provided. You can perform queries on the indexed documents using the query interface.

<p align="center"><img src="./others/gui.jpg" width=500></p>  

## Postgres configuration

Postgres was configured to use a GIN index over the tsvectors of the inserted text, thus allowing better query efficiency. The index is created after the data is loaded. Queries are conducted using tsvectors generated by the stripped version of the documents and the query, and ranked by the plain_to_tsvector() and rank() functions.
## Obtained Results

### Output values:

 You may find that the results emmited by Postgres and our method seldom match up. We are convinced this is because of the fact that the `rank()` function does not use any global information (https://www.postgresql.org/docs/current/textsearch-controls.html), and thus cannot be using the tf_idf method. Furthermore, term extraction on Postgres is fundamentally different that ours, due to our different stopword lists and the fact that Postgres´s tsvectors allow more granular access to information by pointing to where in a document a particular term is found. Finally, the `plain_to_tsquery()` function makes it so that the document has to match all the terms in the query prompt, while our implementation uses plain cosine distance.

### Indexing results

We were able to identify that both our and postgres´s index creation complexity is proportional to O(n). We notice however that postgres´s implementation is considerably more efficient. This is to be expected as our implementation is in python, and still leaves room for algorithmical improvement.

<p align="center"><img src="./others/indexing_performance.jpg" width=500></p>  

### Querying Data

Postgres exhibits a very fast search performance against our solution. We can easily determine our data to signify a O(n) performance, but Postgres is difficult to identify. It would make theoretical sense, however that because of the GIN it would tend to k*log(n), k being the number of query terms and n the ammount of documents.

<p align="center"><img src="./others/log_performance.jpg" width=500></p>  

## License
Distributed under the MIT license. See [`LICENSE`](./LICENSE) for more information.

## Report

### Data Domain Description

*Data type*: Tweets in JSON format contain text (for the content of the tweet) and a unique identifier id after data cleaning.

*Data structure*: Tweets in JSON format usually contain several fields, such as "id" (tweet unique identifier), "created_at" (creation date and time), "text" (tweet content), "user" ( information of the user who published the tweet), "entities" (information about hashtags, mentions, links, etc.), among others.

*Fields and attributes*: Each field in the tweet has a specific meaning. For example, the "id" field stores the unique identifier of the tweet, the "text" field contains the content of the tweet.

*Relationships between data*: In the context of tweets, relationships may exist between the users mentioned, the hashtags used, the replies or retweets made to other tweets, etc.

*Restrictions and rules*: There may be specific restrictions and rules on the tweet data, such as the maximum length of the tweet content, the mandatory nature of certain fields, or the validity of certain values, such as valid user IDs or hashtags.

*Meaning and context*: In the data domain description, it is useful to provide contextual information about the usage of the tweets.

### Backend

# *Construction of the inverted index*: 

### def search_query():
First, it checks if the file exists, preprocesses the query with the preprocesses function, initializes a dictionary called term_frequency that stores the frequency of each term. Then, the tf_idf is calculated, which is the quotient of the frequency of the term and the total number of documents. A list called weight_list is created that stores the weights of each term for each document. If a match is found, the pair (document identifier, term weight) is added to weight_list. If there is no match, a pair (document identifier, 0.0) is added to indicate that the term is not present in that document.
The weights for all terms and documents are sorted, then the result list is trimmed to get the top_k top results. Finally, the sorted results will be returned.

### def processIndexLine():
It splits the line into parts separated by the ":" character and stores the results in a list called 'splitted', assigning the first element of the 'splitted' list to the variable 'term'. We then convert the second element of the 'splitted' list to a floating point number and assign it to the 'idf' variable.
We take the third element of the 'splitted' list, split it into substrings separated by the ';' character, and store the results in a list called 'term_tf_idf_list_str'. Using [:-1] removes the last element of the list, which is empty. An empty list 'term_tf_idf_list' is created which will be used to store pairs of values.
The for loop iterates over each element in the 'term_tfidf_list_str' list and performs various split operations by splitting the substrings.
Finally, the function returns three values: 'term', 'idf', and 'term_tf_idf_list'. 'term' contains the first part of the line, 'idf' contains the second element converted to a floating point number, and 'term_tf_idf_list' contains a list of tuples representing the term and tf-idf values ​​extracted from the line of entrance.
This function processes an input line in a specific format and extracts relevant information from it for later use or storage.

### def index_documents():
The path of the folder where the documents to be indexed are located is established. Open each document file in read mode using a 'with' statement. Reads the content of the file as a JSON object and stores it in the 'x' variable. It extracts the document id from the current line and stores it in the 'doc_id' variable. We increased the counter for the number of indexed documents. The current line is processed using a function called preprocess, it is stored in the 'terms' variable.
The code iterates over each term and frequency in term_frequency using the for term, frequency in term_frequency.items(): loop.
After iterating over all lines and terms in a document, self.inverted_index is checked to see if it contains elements. If so, it means that there is data remaining in the self.inverted_index dictionary that has not yet been written to disk. In this case, the process of ordering and writing the block to disk is repeated.
The function merge_all_blocks is called, which takes as its argument a list of block files located in the "../blocks/" folder and combines all the blocks into a single merged-index block. Finally, we call a build_isam_index() method on the current object, which builds an Indexed Sequential Access Method (ISAM) index based on the generated inverted index.
In simple accounts, it traverses a list of text documents, processes and counts the terms in each document, writes the inverted index blocks to disk, and finally generates a merged inverted index and corresponding ISAM index.

### def build_isam_index():
Create the 'ISAM' index learned in the previous unit of the course.
Reads the inverted index file line by line, builds an ISAM index based on a specified range of lines, and creates a new ISAM index file that maps each term to its offset in bytes in the inverted index file.

# *Secondary Memory Management*
Secondary memory is managed using long-term storage and access techniques, such as disk storage. In the provided code, files on disk are used to store the inverted index and data blocks.

In the index_documents method, each document in the '../documents' directory is read and processed line by line. If the size of the inverted index in memory (self.inverted_index) exceeds the specified limit size (self.BLOCK_SIZE), the current block is written to a file on disk using the 'write_to_disk' function. After writing the block, the inverted index in memory is cleared and the block number (self.block) is incremented. This disk writing process is repeated until all documents are processed.

Once all the documents have been processed, all the blocks stored on disk are merged using the 'merge_all_blocks' function. The 'merge_all_blocks' function merges the blocks into a single merged block, which is then written to the '../spimi_inverted_index.txt' file along with the calculation of the inverted frequency of documents (self.amount_documents).

In the build_isam_index method, the file ‘../spimi_inverted_index.txt’ is read and an ISAM (Indexed Sequential Access Method) index is created in the file ‘../isam_index.txt’. The ISAM index is built by recording the byte offset of each line in the inverted index file. This allows for more efficient access to specific lines of the inverted index file when performing a search.

# *Optimal query execution*

Inverted Index: The inverted index is used to speed up the search for terms in documents.

Efficient document processing: During document indexing, each document is processed line by line and updates the inverted index in blocks.

Block fusion: After processing all the documents, the inverted index blocks stored on disk are merged. This merger combines the blocks into a single block optimized for efficient searches.

Query normalization: We normalize the queries before executing the search. Applying a pre-processing process that includes tokenization and the calculation of term frequencies.

Cosine distance similarity calculation: The cosine distance similarity calculation is used to assign weights to documents based on their relevance to the query.
