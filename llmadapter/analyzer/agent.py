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
            max_tokens= 4000,
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

    def process(self, input_dict_1, input_dict_2,sheetnames):
        # Convert dicts to strings for prompt formatting
        input_dict_1_str = json.dumps(input_dict_1, indent=2)
        input_dict_2_str = json.dumps(input_dict_2, indent=2)
        messages = self.prompt_template.format_messages(
            data_dict_fixed=input_dict_1_str,
            country_dict=input_dict_2_str,
            sheetnames = sheetnames
        )

        response = self.llm(messages).content

        # Optional: Try to convert output string back to dictionary
        try:
            output_dict = json.loads(response)
            return output_dict
        except json.JSONDecodeError:
            return {"error": "Failed to parse LLM output as JSON", "raw_output": response}
