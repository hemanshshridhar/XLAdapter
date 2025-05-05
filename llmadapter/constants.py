import os

DUO_E_MODEL_ID = "00ae0955-31bb-4e92-abba-6006ccd0e78a"

# class AzureConstants:
#     LLM_SAS_URL = os.environ.get("LLM_SAS_URL")

class ExceptionMessages:
    BLOB_PATH_ERROR = "Blob path cannot be empty or None"

class LLMConstants:
    GPT_41_MINI_MODEL = "gpt-4.1-mini"
    GPT_4o_MODEL = "gpt-4o"
    TEMPERATURE = 0
    MAX_TOKENS = 4000
    MAX_RETRIES = 10
    STREAMING = True
    TAGS = ["final_response_generator"]

# class DBConfig:
#     DBNAME = os.environ.get("DBNAME")
#     USER = os.environ.get("USER")
#     PASSWORD = os.environ.get("PASSWORD")
#     HOST = os.environ.get("HOST")
#     PORT = os.environ.get("PORT")

class Status:
    SUCCESS = "success"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
