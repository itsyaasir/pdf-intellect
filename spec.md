
---

## Code Overview

The project mainly consists of two Python scripts: `index.py` and `pdf_processor.py`.

- `index.py` is a CLI tool for indexing PDFs and searching for similar content. It uses the Click library to handle command-line interfaces.
  
- `pdf_processor.py` contains the main functionality for processing PDF files. It utilizes Sentence Transformers to convert sentences into embeddings, stores the embeddings and additional metadata in a PostgreSQL database, and provides a function for searching similar content based on these embeddings.

Additionaly, there are two shell scripts that are used for setting up the environment and the database:

- `conda_setup.sh` creates a Conda environment and installs the necessary Python packages.
  
- `db_setup.sh` creates a PostgreSQL database, installs the necessary PostgreSQL extensions, and creates a table for storing document embeddings and metadata.

## Further Improvements and Contributions

While the current implementation provides basic functionality for indexing and searching PDF files based on embeddings, there are several ways in which the project could be further improved:

- The text extraction process could be improved to handle more complex PDF files, such as those containing tables, images, or other non-text elements.
  
- Additional metadata could be extracted from the PDF files and stored in the database, such as author information, publication date, etc.
  
- The search function could be enhanced to provide more advanced search options, such as searching within a certain date range or by a certain author.
  
- The performance and efficiency of the embedding process could potentially be improved by using a different model, or by parallelizing the embedding process.
  
If you would like to contribute to this project, please feel free to fork the repository and submit a pull request. Please ensure that your code is well-commented, follows the existing style, and includes any necessary tests.

## Disclaimer

This project is intended for educational and experimental purposes. It may not be suitable for production use without further testing and development. Use at your own risk.

## License

This project is licensed under the terms of the MIT license. For more information, see the [LICENSE](LICENSE) file.

---
