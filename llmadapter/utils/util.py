from pathlib import Path
from docx import Document
from PyPDF2 import PdfReader
import shutil
import os
import json
import tiktoken


def delete_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"Deleted folder: {folder_path}")
    else:
        print(f"Folder does not exist for cleanup: {folder_path}")

def delete_paths(file_paths):
    top_level_folders = {path.split("/")[0] for path in file_paths if "/" in path}

    for folder in top_level_folders:
        delete_folder(folder)

def get_file_content(file_path):
    ext = Path(file_path).suffix.lower()

    if ext == '.docx':
        doc = Document(file_path)
        content = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        return content.strip()

    elif ext == '.pdf':
        try:
            reader = PdfReader(file_path)
            content = "\n".join(page.extract_text() or "" for page in reader.pages)
            return content.strip()
        except Exception as e:
            raise RuntimeError(f"Failed to read PDF: {e}")

    elif ext == '.txt' or ext == '.md':
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
        
    elif ext == '.json':
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

def count_tokens(text):
    encoding = tiktoken.get_encoding("o200k_base")
    tokens = encoding.encode(text)
    return len(tokens)
