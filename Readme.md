
---

# PDF Embedding Indexer

PDF Embedding Indexer is a CLI tool designed to process text content from PDF files, generate meaningful embeddings from the text using Sentence Transformers, and store those embeddings in a PostgreSQL database. This allows for quick and efficient similarity searching, providing a useful tool for managing and navigating through a large number of PDF files.

## Features

- Extracts text content from PDF files and generates embeddings using Sentence Transformers.
- Stores the embeddings in a PostgreSQL database for quick and efficient similarity searching.
- Allows for sentence-level indexing, offering granular search results.
- Stores additional metadata for each document, including file hash, timestamp, and title.
- Prevents duplicate PDFs from being indexed.

## Requirements

- Python 3.8 or higher
- PostgreSQL
- [sentence-transformers](https://github.com/UKPLab/sentence-transformers)
- psycopg2-binary
- sqlalchemy
- pgvector
- python-magic
- pdfminer.six
- nltk

## Setup

1. Ensure that you have Python 3.8 or higher installed.

2. Install PostgreSQL and setup a database for this project.

3. Clone this repository:

    ```bash
    git clone https://github.com/itsyaasir/pdf-embedding-indexer.git
    ```

4. Change into the project directory:

    ```bash
    cd pdf-embedding-indexer
    ```

5. You can create and activate a Conda or a virtual environment:

    - For Conda environment:

        Run the provided setup script to create a Conda environment and install the necessary packages:

        ```bash
        bash conda_setup.sh
        ```

    - For virtual environment:

        Create a virtual environment:

        ```bash
        python -m venv venv
        ```

        Activate the virtual environment:
        - On Unix or MacOS, run:

            ```bash
            source venv/bin/activate
            ```

        - On Windows, run:

            ```bash
            venv\Scripts\activate
            ```

        Install the required packages:

        ```bash
        pip install -r requirements.txt
        ```

6. Run the provided setup script to setup the database:

    ```bash
    bash db_setup.sh
    ```

7. Modify the database parameters (`DB_PARAMS`) in `index.py` if necessary.

## Usage

To index a PDF:

```
python index.py index <pdf_file>
```

To search for similar content given a query:

```
python index.py search "<query>"
```

These commands will print their results to the console.

## Contributing

Please feel free to fork this repository and contribute. When submitting your changes, please ensure that your code is well-commented and that you have tested your changes.

## License

This project is licensed under the terms of the MIT license. See [LICENSE](LICENSE) for more details.

---
