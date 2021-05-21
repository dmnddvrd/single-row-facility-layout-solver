from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

def get(key):
    return os.getenv(key.upper())