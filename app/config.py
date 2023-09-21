from dotenv import load_dotenv
import os

load_dotenv()

DB_PARAMS = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),  # adjust if your DB is not on localhost
}


CONNECTION_STRING = f"postgresql+psycopg2://{DB_PARAMS['user']}:{DB_PARAMS['password']}@{DB_PARAMS['host']}:{DB_PARAMS['port']}/{DB_PARAMS['dbname']}"


LLM_MODEL_PATH = "../models/llama-2-7b-chat.Q4_K_M.gguf"


EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
