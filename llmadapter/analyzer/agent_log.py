from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate as Sys,
    HumanMessagePromptTemplate as Hum,
)
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import json


class AnalyzerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            max_tokens=8000,
            max_retries=10,
            streaming=False,
            tags=["final_response_generator"],
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                Sys(prompt=PromptTemplate([], SYSTEM_PROMPT)),
                Hum(prompt=PromptTemplate(
                    ["data_dict_fixed", "country_dict", "sheetnames"],
                    USER_PROMPT,
                )),
            ]
        )

    # -----------------------------------------------------------------
    def process(self, model_dict, country_dict, sheetnames):
        """
        Returns
        -------
        {
          "output_dict": {sheet:{addr:new_value}},
          "log_table":   list[ [Sheet, Field, Address, Old, New] ]
        }
        """
        messages = self.prompt.format_messages(
            data_dict_fixed=json.dumps(model_dict, indent=2),
            country_dict=json.dumps(country_dict, indent=2),
            sheetnames=json.dumps(sheetnames),
        )

        raw = self.llm.invoke(messages).content

        try:
            obj = json.loads(raw)
            assert "output_dict" in obj and "log_table" in obj
            return obj
        except Exception as e:
            return {
                "error": f"Failed to parse or missing keys: {e}",
                "raw_output": raw,
            }
