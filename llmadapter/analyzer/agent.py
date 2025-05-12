from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate as SystemTemplate,
    HumanMessagePromptTemplate as HumanTemplate,
)
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

import json


class AnalyzerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model= "gpt-4o",
            temperature=0,
            max_tokens= 8000,
            max_retries= 10,
            streaming=False,
            tags= ["final_response_generator"]
        )
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemTemplate(
                    prompt=PromptTemplate(input_variables=[], template=SYSTEM_PROMPT)
                ),
                 HumanTemplate(
                    prompt=PromptTemplate(
                        input_variables=["data_dict_fixed", "country_dict", "sheetnames"],
                        template=USER_PROMPT
                    )
                ),
            ]
        )

    def process(self, input_dict_1, input_dict_2, sheetnames):
        """
        Returns
        -------
        {
          "output_dict": {sheet: {addr: new_value}},
          "log_table":   [ {Sheet Name, Cell Field, Cell Address, Previous Value, New Value}, ... ]
        }
        """

        model_str   = json.dumps(input_dict_1, indent=2)
        country_str = json.dumps(input_dict_2, indent=2)

        messages = self.prompt_template.format_messages(
            data_dict_fixed=model_str,
            country_dict=country_str,
            sheetnames=json.dumps(sheetnames),
        )


        response = self.llm.invoke(messages).content

        try:
            obj = json.loads(response)
        except json.JSONDecodeError as e:
            return {"error": f"JSON decode error: {e}", "raw_output": response}

        if "output_dict" not in obj:
            return {"error": "Key 'output_dict' missing", "raw_output": obj}

        # Accept both "log_table" (flat) and "log_tables" (nested)
        if "log_table" in obj:
            log_table = obj["log_table"]

        elif "log_tables" in obj:
            # convert nested dict → flat list
            log_table = []
            for sheet, field_map in obj["log_tables"].items():
                for label, meta in field_map.items():
                    log_table.append(
                        {
                            "Sheet Name":     sheet,
                            "Cell Field":     label,
                            "Cell Address":   meta.get("address"),
                            "Previous Value": meta.get("old_value"),
                            "New Value":      meta.get("new_value"),
                        }
                    )
        else:
            return {"error": "No change-log key found", "raw_output": obj}

        return {"output_dict": obj["output_dict"], "log_table": log_table}
