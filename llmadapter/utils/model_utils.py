import os
import json
import tiktoken
from .util import get_file_content, count_tokens


def get_sheet_names(file_path):
    json_data = get_file_content(file_path)
    sheet_names = [sheet['name'].replace(" ", "_") for sheet in json_data['sheets']]
    return sheet_names

def split_sheets(input_dir, output_dir):
    data = get_file_content(input_dir)
    os.makedirs(output_dir, exist_ok=True)    
    
    for sheet in data["sheets"]:
        sheet_name = sheet["name"].replace(" ", "_")
        output_path = os.path.join(output_dir, f"{sheet_name}.json")
        
        sheet_data = {
            "workbook_name": data["workbook_name"],
            "sheet": sheet
        }

        with open(output_path, "w") as output_file:
            json.dump(sheet_data, output_file, indent=4)

        print(f"Saved {output_path}")

def print_tokens(input_dir):
    print(f"{'Filename'.ljust(30)} | {'Tokens'}")
    print("-" * 40)

    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(input_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            token_count = count_tokens(content)
            print(f"{filename.ljust(30)} | {token_count}")

def load_trimmed_content(content, token_count):
    encoding = tiktoken.get_encoding("o200k_base")
    tokens = encoding.encode(content)
    
    if token_count < 10000:
        return content
    elif 10000 <= token_count <= 500000:
        percentage = 0.05
    else:
        percentage = 0.02

    trimmed_token_count = int(token_count * percentage)
    trimmed_tokens = tokens[:trimmed_token_count]
    return encoding.decode(trimmed_tokens)

def process_json_files(folder_path, output_file):
    final_document = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                raw_content = f.read()
                token_count = count_tokens(raw_content)

                trimmed_content = load_trimmed_content(raw_content, token_count)
                sheetname = os.path.splitext(filename)[0]
                final_document += f"- **{sheetname}**:\n{trimmed_content}\n\n"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_document)
