import pandas as pd
from openpyxl import load_workbook
from typing import Dict, List, Any
import json

class SheetEncoder:
    def __init__(self):
        pass

    def encode_sheet_with_formula_and_value(self, filename: str, sheet_names: List[str] = None) -> str:
        """
        Extracts values, formulas, and cell addresses from specified sheets
        of an Excel file and returns a structured JSON string.
        """
        wb_formula = load_workbook(filename, keep_vba=True)
        wb_value = load_workbook(filename, data_only=True)

        if sheet_names is None:
            sheet_names = wb_formula.sheetnames

        excel_data = {
            "workbook_name": filename,
            "sheets": []
        }

        for sheet_name in sheet_names:
            if sheet_name not in wb_formula.sheetnames:
                print(f"Warning: Sheet '{sheet_name}' not found in workbook.")
                continue

            sheet_formula = wb_formula[sheet_name]
            sheet_value = wb_value[sheet_name]

            sheet_data = {
                "name": sheet_name,
                "cell_data": []
            }

            for row in sheet_formula.iter_rows():
                for cell_formula in row:
                    coord = cell_formula.coordinate
                    cell_value = sheet_value[coord]

                    if cell_formula.value is None and cell_value.value is None:
                        continue

                    cell_info = {
                        "address": coord,
                        "value": cell_value.value,
                        "formula": str(cell_formula.value) if cell_formula.data_type == 'f' else None
                    }

                    sheet_data["cell_data"].append(cell_info)

            excel_data["sheets"].append(sheet_data)

        return json.dumps(excel_data, indent=4)

    def extract_parameter_dict_from_excel(self, sheet_path: str) -> Dict[str, Dict[str, Any]]:
        """
        Extracts a nested dictionary from an Excel sheet of the form:
        {
            "SheetName": {
                "Parameter Name": "Mean Value"
            }
        }
        """
        wb = load_workbook(sheet_path, data_only=True)
        ws = wb.active  # Use the first sheet

        raw_data = []
        for row in ws.iter_rows(values_only=True):
            raw_data.append(row)

        df = pd.DataFrame(raw_data)

        df = df.iloc[2:, [2, 3, 4]]  # Columns C, D, E
        df.columns = ['sheet_name', 'parameter', 'value']
        df['sheet_name'] = df['sheet_name'].fillna(method='ffill')
        df = df.dropna(subset=['parameter'])

        structured_dict = {}
        for _, row in df.iterrows():
            sheet = row['sheet_name']
            param = row['parameter']
            val = row['value']
            structured_dict.setdefault(sheet, {})[param] = val

        return structured_dict

    def write_to_sheet(
        self,
        output_dict: Dict[str, Dict[str, Any]],
        template_path: str,
        output_path: str,
        keep_vba: bool = True
    ):
        """
        Write `output_dict` back into a copy of `template_path`
        and save it to `output_path`.

        output_dict format:
            {
              "Sheet1": {"70": ["H14"], "7.5": ["H15"]},
              "Sheet2": {...}
            }
        """
        wb = load_workbook(template_path, keep_vba=keep_vba)

        for sheet_name, sheet_data in output_dict.items():
            if sheet_name not in wb.sheetnames:
                raise ValueError(f"Sheet '{sheet_name}' not found in workbook.")
            ws = wb[sheet_name]
            for val, cell_list in sheet_data.items():
                for addr in cell_list:
                    ws[addr].value = val

        wb.save(output_path)
