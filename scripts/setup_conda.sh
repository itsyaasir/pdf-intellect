#!/bin/bash

# Create the conda environment
conda create --name pdf-intellect python=3.8 -y

# Activate the conda environment
source activate pdf-intellect

# Install PyTorch, torchvision, and torchaudio with conda
conda install -c pytorch torch torchvision torchaudio -y

# Install FAISS with conda
conda install -c pytorch faiss-cpu -y

# Install other necessary packages with pip
pip3 install sentence-transformers psycopg2-binary sqlalchemy pgvector python-magic pdfminer.six nltk tabulate langchain dotenv python-dotenv pypdf llama-cpp-python
