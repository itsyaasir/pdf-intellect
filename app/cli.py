"""
This module contains the CLI for the PDF processor.
"""

import textwrap
import click
import config
from app.llama import LLMWrapper
from app.processor import PDFProcessor


pdf_processor = PDFProcessor(embedding_model=config.EMBEDDING_MODEL)


@click.group()
def cli():
    """
    CLI for the PDF processor.
    """


@click.command()
@click.argument("pdf_file")
def index(pdf_file):
    """
    Index a PDF file.

    :param pdf_file: The path to the PDF file.

    """
    pdf_processor.process_pdf(pdf_file)


@click.command()
@click.argument("string")
def search(string: str):
    """
    Search for a string in the PDF documents.

    :param search_str: The string to search for.

    """
    results = pdf_processor.search_str(string)
    for result in results:
        response = textwrap.wrap(result.page_content, width=70)
        print("-" * 80)
        print(response)


@click.command()
@click.argument("prompt")
def query(prompt: str):
    """
    Query the LLM based on the content found in the PDF documents.

    :param content: The content to search in the PDF documents.
    :param prompt: The prompt for the LLM based on the content found.

    """
    # Search for the topic in the database
    context = pdf_processor.search_str(prompt)

    llm = LLMWrapper(
        model_path=config.LLM_MODEL_PATH,
    )

    llm_result = llm.query_llm(prompt, context)

    print(llm_result)


cli.add_command(index)
cli.add_command(search)
cli.add_command(query)
