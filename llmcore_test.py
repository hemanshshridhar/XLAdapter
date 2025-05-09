from llmadapter.main import LLMadapt
import asyncio
import time

input_data_model_setup = {
    "model_name": "Early Cost Effectiveness Model: Olaparib vs Comparator Therapies Based on DUO-E",
    "model_id": "00ae0955-31bb-4e92-abba-6006ccd0e78a",
    "model_excel_path": "/content/drive/MyDrive/txt_data/DUO-E - Early Cost-Effectiveness Model with Dummy Data 30 Oct 2023_OWSA trial_SM.xlsm",
    "sheets_path": "/content/drive/MyDrive/txt_data/Input sheet for adapter.xlsm",
    "output_excel_path" : "/content/drive/MyDrive/txt_data/modified.xlsm",
    
}






def model_setup(input_data_model_setup):
    llmcore = LLMCore()
    status = llmcore.model_setup(input_data_model_setup)
    if status:
        print("Model setup successfull.")
    else:
        print("Model setup failed.")



def main():
    start_time = time.time()
    # setup()
    model_setup(input_data_model_setup)
    # asyncio.run(chat_stream(input_data_chat))
    print(f"Time: {time.time() - start_time}")

if __name__ == "__main__":
    main()
