import pandas as pd
from openpyxl import load_workbook
from typing import Dict, List, Any


class SheetEncoder:
    def __init__(self):
        pass

    def encode_sheet(self, filename: str, sheetnames: List[str]) -> Dict[str, Any]:
        """
        Extracts values and their cell addresses from each given sheet and
        returns a structured dictionary.
        """
        wb_value = load_workbook(filename, data_only=True)

        result = []

        for sheet_name in sheetnames:
            if sheet_name not in wb_value.sheetnames:
                raise ValueError(f"Sheet '{sheet_name}' not found in {filename}")

            sheet_value = wb_value[sheet_name]
            sheet_data = self._encode(sheet_value)
            sheet_data = sheet_data.dropna(subset=["Value"])

            sheet_dictionary = {}

            for _, row in sheet_data.iterrows():
                val = str(row["Value"])
                addr = row["Address"]

                if val in sheet_dictionary:
                    sheet_dictionary[val].append(addr)
                else:
                    sheet_dictionary[val] = [addr]

            
            sheet_dictionary = {k: v for k, v in sheet_dictionary.items() if k.lower() != "nan"}

            result.append({
                "sheet_name": sheet_name,
                "data": sheet_dictionary
            })

        return result

    def _encode(self, sheet) -> pd.DataFrame:
        """
        Encodes a single worksheet's values and cell addresses.
        """
        markdown = pd.DataFrame(columns=['Value', 'Address'])

        for row in sheet.iter_rows():
            for cell in row:
                coord = cell.coordinate
                if cell.value is None:
                    continue

                new_row = pd.DataFrame([[cell.value, coord]], columns=markdown.columns)
                markdown = pd.concat([markdown, new_row], ignore_index=True)

        return markdown

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
                    ws[addr].value = val  # overwrite (or create) value

        wb.save(output_path)    