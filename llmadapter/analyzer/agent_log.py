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
            max_tokens= 20000,
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
    # Convert dicts to strings for prompt formatting
    input_dict_1_str = json.dumps(input_dict_1, indent=2)
    input_dict_2_str = json.dumps(input_dict_2, indent=2)
    messages = self.prompt_template.format_messages(
        data_dict_fixed=input_dict_1_str,
        country_dict=input_dict_2_str,
        sheetnames=sheetnames
    )

    response = self.llm(messages).content

    try:
        output_dict = json.loads(response)
    except json.JSONDecodeError:
        return {
            "error": "Failed to parse LLM output as JSON",
            "raw_output": response
        }


    log_table = []
    for sheet, cell_map in output_dict.items():
        for value, addresses in cell_map.items():
            for addr in addresses:
                # Try to find the field that matches this value in input_dict_2
                matched_field = None
                for field, field_value in input_dict_2.items():
                    if str(field_value) == str(value):
                        matched_field = field
                        break

                # Find previous value from input_dict_1 if available
                prev_val = None
                for existing_val, existing_addrs in input_dict_1.get(sheet, {}).items():
                    if addr in existing_addrs:
                        prev_val = existing_val
                        break

                log_table.append({
                    "Sheet Name": sheet,
                    "Cell Field": matched_field or "Unknown",
                    "Previous Value": prev_val,
                    "New Value": value
                })

    return {
        "output_dict": output_dict,
        "log_table": log_table
    }
