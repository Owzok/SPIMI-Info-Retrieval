<br>
<p align="center">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Circle-icons-rocket.svg/1200px-Circle-icons-rocket.svg.png" alt='Logo' width=80 height=80>

<h3 align="center">SPIMI Search Engine</h3>

<p align="center">
    Single-Pass In-Memory Indexing for information search and recovery
</p>

#
<p align="center"

![si](https://camo.githubusercontent.com/3e47acbf09cde3b0ad08c991a390ce5b57d457f95db0154831d95ab094d7bd02/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f41636164656d6963616c25323050726f6a6563742d5965732d73756363657373) ![si](https://camo.githubusercontent.com/7234f85510f85db1deddffb4d8acead60b88f6d6cbb89992ad616235e1816c0b/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4d616465253230576974682d507974686f6e2d626c7565)  ![si](https://img.shields.io/badge/License-MIT-red)

<p align="center"

The **SPIMI** *(Single-Pass In-Memory Indexing)* project is a simple implementation of an indexing algorithm used in information retrieval systems. This project aims to demonstrate the basic concepts of building an inverted index using the SPIMI algorithm.
</p>

## Features
- Building an inverted index from a collection of documents.
- Support for tokenization, stop word removal, and stemming.
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