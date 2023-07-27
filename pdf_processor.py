import os
import glob
import logging
import numpy as np
from sentence_transformers import SentenceTransformer, util
from pdfminer.high_level import extract_text
import psycopg2
import nltk
from nltk.tokenize import sent_tokenize
import json
import datetime
import hashlib
import re
from tabulate import tabulate


def get_punkt():
    try:
        sent_tokenize("dummy")
    except LookupError:
        nltk.download("punkt")


class PDFProcessor:
    def __init__(self, db_params):
        self.model = SentenceTransformer("all-mpnet-base-v2")
        self.conn = psycopg2.connect(**db_params)
        self.cursor = self.conn.cursor()

        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        self.logger.addHandler(handler)

        get_punkt()

    def process_pdf(self, pdf_file):
        try:
            # Compute the hash of the file
            file_hash = self.compute_file_hash(pdf_file)

            # Check if the file has already been indexed
            self.cursor.execute(
                "SELECT 1 FROM documents WHERE metadata->>'file_hash' = %s", [file_hash]
            )
            if self.cursor.fetchone() is not None:
                self.logger.error(f"File {pdf_file} has already been indexed.")
                return

            fileName = os.path.basename(pdf_file)
            title = fileName[:-4].replace(" ", "_")

            text = extract_text(pdf_file)
            sentences = sent_tokenize(text)
            sentences = [
                self.clean_sentence(sentence) for sentence in sentences if sentence
            ]

            embeddings = self.model.encode(
                sentences,
                show_progress_bar=True,
            )

            data = [
                (
                    embedding.tolist(),
                    sentence,
                    json.dumps(
                        {
                            "file_hash": file_hash,
                            "timestamp": datetime.datetime.utcnow().isoformat(),
                            "title": title,
                        }
                    ),
                )
                for sentence, embedding in zip(sentences, embeddings)
            ]

            self.cursor.executemany(
                "INSERT INTO documents (embedding, content, metadata) VALUES (%s, %s, %s)",
                data,
            )

            self.conn.commit()  # commit after each PDF processing to save changes
            self.logger.info(f"Processed and indexed {pdf_file}")
        except psycopg2.Error as e:
            self.conn.rollback()  # rollback the transaction if any error occurs
            self.logger.error(f"Database error while processing {pdf_file}: {e}")
        except Exception as e:
            self.logger.error(f"Error while processing {pdf_file}: {e}")

        finally:
            self.cursor.close()
            self.conn.close()

    def search(self, query):
        embedding = self.model.encode([query])[0]
        embedding_query = ",".join([str(x) for x in embedding])
        embedding_query = f"[{embedding_query}]"

        self.cursor.execute(
            """
             SELECT content, 1 - (embedding <=> '"""
            + embedding_query
            + """') AS cosine_similarity
            FROM documents
            ORDER BY cosine_similarity DESC
            LIMIT 10
            """,
        )
        results = self.cursor.fetchall()
        table = tabulate(
            results,
            headers=["Sentence", "Cosine Similarity"],
            tablefmt="orgtbl",
            showindex=True,
        )
        return table

    @staticmethod
    def compute_file_hash(file_path):
        hasher = hashlib.sha256()
        with open(file_path, "rb") as file:
            while chunk := file.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    @staticmethod
    def clean_sentence(sentence):
        sentence = re.sub(
            r"\s+", " ", sentence
        )  # Replace all whitespace characters with a space
        return sentence.strip()  # Trim the sentence
