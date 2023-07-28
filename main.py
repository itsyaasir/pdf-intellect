from app.cli import cli
from app.logger import setup_logger


if __name__ == "__main__":
    # Set up logging
    setup_logger()
    cli()
