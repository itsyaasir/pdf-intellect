"""
This module contains utility functions.
"""

import hashlib
import logging
from typing import List
import nltk
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders.pdf import PyPDFLoader
from nltk.tokenize import sent_tokenize

logger = logging.getLogger(__name__)


def compute_file_hash(file_path):
    """
    Compute the hash of a file.
    """
    hasher = hashlib.sha256()
    with open(file_path, "rb") as file:
        while chunk := file.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def convert_pdf_to_text(pdf_file) -> List[str]:
    """
    Convert a PDF file to a list of strings, one for each page.

    :param pdf_file: The path to the PDF file.
    :return: A list of strings, one for each page.

    """
    pdf_doc = PyPDFLoader(pdf_file)
    page_content: List[str] = []
    for page in pdf_doc.load():
        try:
            page_content.append(page.page_content)

        except Exception as err:
            logger.error("Error while converting pdf to text %s: %s", pdf_file, err)

    return page_content


def split_text(page_str: List[str]) -> List[str]:
    """
    Split a list of strings into a list of sentences.

    :param page_str: A list of strings, one for each page.
    :return: A list of sentences.

    """
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=0,
            length_function=len,
        )

        split_text_list = []

        for text in page_str:
            split_text_list.extend(
                text_splitter.split_text(
                    text.replace("\x00", "\uFFFD")
                )  # Replace null bytes
            )

        return split_text_list

    except Exception as err:
        logger.error("Error while splitting text: %s", err)
        return []


def get_punkt():
    """
    Download the Punkt tokenizer if it is not already downloaded.
    """
    try:
        sent_tokenize("dummy")
    except LookupError:
        nltk.download("punkt")
