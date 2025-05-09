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
            model="gpt-4o",
            temperature=0,
            max_tokens=20000,
            max_retries=10,
            streaming=False,
            tags=["final_response_generator"]
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

        # Format prompt
        messages = self.prompt_template.format_messages(
            data_dict_fixed=input_dict_1_str,
            country_dict=input_dict_2_str,
            sheetnames=sheetnames
        )

        # LLM call
        response = self.llm(messages).content

        # Try parsing LLM output
        try:
            output_dict = json.loads(response)
        except json.JSONDecodeError:
            return {
                "error": "Failed to parse LLM output as JSON",
                "raw_output": response
            }

        # Reverse lookup: (sheet, address) -> old value
        address_to_old_value = {}
        for sheet, val_map in input_dict_1.items():
            for old_val, addr_list in val_map.items():
                for addr in addr_list:
                    address_to_old_value[(sheet, addr)] = old_val

        # Construct log table
        log_table = []
        for sheet, fields in input_dict_2.items():
            for field, new_value in fields.items():
                new_value_str = str(new_value)

                # Get suggested addresses from LLM output
                addresses = []
                if sheet in output_dict:
                    for val_str, addr_list in output_dict[sheet].items():
                        if str(val_str) == new_value_str:
                            addresses = addr_list
                            break

                for addr in addresses:
                    prev_val = address_to_old_value.get((sheet, addr))
                    log_table.append({
                        "Sheet Name": sheet,
                        "Cell Field": field,
                        "Cell Address": addr,
                        "Previous Value": prev_val,
                        "New Value": new_value
                    })

        return {
            "output_dict": output_dict,
            "log_table": log_table
        }
