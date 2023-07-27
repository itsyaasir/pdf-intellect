import click
import logging
from pdf_processor import PDFProcessor


DB_PARAMS = {
    "dbname": "vector_db",
    "user": "yasirdev",
    "password": "",
    "host": "localhost",  # adjust if your DB is not on localhost
}

processor = PDFProcessor(DB_PARAMS)


@click.group()
def cli():
    pass


@click.command()
@click.argument("pdf_file")
def index(pdf_file):
    processor.process_pdf(pdf_file)


@click.command()
@click.argument("query")
def search(query):
    results = processor.search(query)
    for result in results:
        print(f"{result[0]} (Score: {round(result[1], 4)})")


cli.add_command(index)
cli.add_command(search)

if __name__ == "__main__":
    # Set up logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

    cli()
