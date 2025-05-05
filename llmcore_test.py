from llmcore.main import LLMCore
import asyncio
import time

input_data_model_setup = {
    "model_name": "Early Cost Effectiveness Model: Olaparib vs Comparator Therapies Based on DUO-E",
    "model_id": "00ae0955-31bb-4e92-abba-6006ccd0e78a",
    "model_excel_path": "00ae0955-31bb-4e92-abba-6006ccd0e78a/DUO-E - Early Cost-Effectiveness Model with Dummy Data 30 Oct 2023_OWSA trial_SM 2.xlsm",
    "report_doc_path": "00ae0955-31bb-4e92-abba-6006ccd0e78a/Filtered DUO-E report for model analyser tool.docx",
    "sheets_desc_doc_path": "00ae0955-31bb-4e92-abba-6006ccd0e78a/Sheetwise details.docx",
}

input_data_chat = {
    "model_id": "00ae0955-31bb-4e92-abba-6006ccd0e78a",
    "query": "give me upper and lower bound of all unit cost type parmeters.",
    "chat_history": [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hello, How can I help you?"}
    ]
}


def setup():
    llmcore = LLMCore()
    status = llmcore.db_setup()
    if status:
        print("DB Setup Successfully.") 
    else:
        print("DB setup failed.")

def model_setup(input_data_model_setup):
    llmcore = LLMCore()
    status = llmcore.model_setup(input_data_model_setup)
    if status:
        print("Model setup successfull.")
    else:
        print("Model setup failed.")

async def chat_stream(input_data_chat):
    llmcore = LLMCore()
    response_generator = llmcore.chat_stream(input_data_chat)
    msg = ''
    async for chunk in response_generator:
        # print(chunk)
        if chunk['content'] == "|<start>|" or chunk['content'] == "|<end>|":
            pass
        elif chunk['type'] == "response":
            msg += chunk['content']
    print(f"Message: {msg}")

def main():
    start_time = time.time()
    # setup()
    model_setup(input_data_model_setup)
    # asyncio.run(chat_stream(input_data_chat))
    print(f"Time: {time.time() - start_time}")

if __name__ == "__main__":
    main()