<br>
<p align="center">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Circle-icons-rocket.svg/1200px-Circle-icons-rocket.svg.png" alt='Logo' width=80 height=80>

<h3 align="center">SPIMI Search Engine</h3>

<p align="center">
    Single-Pass In-Memory Indexing for information search and recovery
</p>

#
<p align="center"

![ga](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![si](https://img.shields.io/badge/Academical%20Project-Yes-brightgreen?style=for-the-badge&logo=awesomewm) ![si](https://img.shields.io/badge/License-MIT-red?style=for-the-badge&logo=dpd)

<p align="center"

The **SPIMI** *(Single-Pass In-Memory Indexing)* project is a simple implementation of an indexing algorithm used in information retrieval systems. This project aims to demonstrate the basic concepts of building an inverted index using the SPIMI algorithm.
</p>

## Features
- Building an inverted index from a collection of documents.
- Support for tokenization, stop word removal, and stemming.
- ISAM indexation for search optimization.
- Querying the inverted index to retrieve relevant documents.

### Prerequisites

To run the SPIMI index project, you need to have the following installed:
- Python (version 3.6 or higher)
- NLTK (Natural Language Toolkit) library
- Pygame (SDL wrapped library)

### Installation

1. Clone the repository to your local machine:
```shell
git clone https://github.com/your-username/spimi-index-project.git
```

2. Install the required dependencies:
```sh
pip install nltk
```

3. Download the necessary NLTK resources:
```py
import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('snowball_data')
```

## Usage
1. Prepare your collection of documents in a suitable format (e.g., plain text files) and put them into the documents folder.

2. Update the ```main.py``` file with the appropriate configuration parameters and paths to your document collection.

3. Run the ```main.py``` script to build the inverted index:

```sh
python main.py
```

4. After attempting a search, the index is built, you can perform queries on the indexed documents using the provided query interface.

<p align="center"><img src="./others/gui.png" width=500></p>  


## Contributing

Contributions to the SPIMI index project are welcome! If you find any bugs, have feature requests, or would like to make improvements, please feel free to open an issue or submit a pull request.

## License
Distributed under the MIT license. See [`LICENSE`](./LICENSE) for more information.