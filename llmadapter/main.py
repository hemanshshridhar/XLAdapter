import os
from llmadapter.analyzer.agent import AnalyzerAgent
from llmadapter.utils.blob_storage_util import BlobStorageUtil
from llmadapter.utils.notifier import send_setup_notification
from llmadapter.utils.util import delete_folder
from llmadapter.tools.sheetencoder import SheetEncoder
from .constants import Status


class LLMadapt:
    def __init__(self):
        self.analyzer = AnalyzerAgent()
        self.sheet_encoder = SheetEncoder()

    def model_setup(self, input_data_model_setup):
        model_id          = input_data_model_setup.get("model_id")
        base_excel_path   = input_data_model_setup.get("model_excel_path")
        country_excel_path= input_data_model_setup.get("sheets_path")
        output_excel_path = input_data_model_setup.get("output_excel_path")
        # ←—— grab your list here
        sheetnames        = input_data_model_setup.get("sheetnames", [])

        print(f"[INFO] Starting model setup for: {model_id}")

        try:
            # pass sheetnames through
            output_path = self.compare_and_generate_updated_xlsm(
                base_file_path    = base_excel_path,
                country_file_path = country_excel_path,
                output_file_path  = output_excel_path,
                sheetnames        = sheetnames,
            )
            print(f"[SUCCESS] Model setup completed for: {model_id}")
        except Exception as e:
            print(f"[FAILED] Model setup failed for: {model_id} — {e}")
            raise
        # finally:
        #     temp_dir = os.path.dirname(base_excel_path)
        #     if os.path.exists(temp_dir):
        #         rmtree(temp_dir, ignore_errors=True)

        return output_path

    def compare_and_generate_updated_xlsm(
        self,
        base_file_path: str,
        country_file_path: str,
        output_file_path: str,
        sheetnames: list,            # ←—— make sure this param is here
    ):
        """
        Compare two .xlsm files via LLM, generate a result dictionary, and write it to a new .xlsm file.
        """
        # Step 1: Convert Excel sheets to dictionaries
        model_dict   = self.sheet_encoder.encode_sheet(base_file_path,    sheetnames)
        country_dict = self.sheet_encoder.encode_sheet(country_file_path, sheetnames)
        output_dict  = self.analyzer.process(model_dict, country_dict)
        print(output_dict)
        # Step 3: Write the result to new Excel file
        self.sheet_encoder.write_to_sheet(
            output_dict    = output_dict,
            template_path  = base_file_path,
            output_path    = output_file_path
        )

        return output_file_path