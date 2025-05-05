from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate as SystemTemplate,
    HumanMessagePromptTemplate as HumanTemplate,
)
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from llmadapter.constants import LLMConstants
from .template import SYSTEM_PROMPT, USER_PROMPT
import json


class AdapterAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=LLMConstants.GPT_41_MINI_MODEL,
            temperature=LLMConstants.TEMPERATURE,
            max_tokens=LLMConstants.MAX_TOKENS,
            max_retries=LLMConstants.MAX_RETRIES,
            streaming=False,
            tags=LLMConstants.TAGS
        )
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemTemplate(
                    prompt=PromptTemplate(input_variables=[], template=SYSTEM_PROMPT)
                ),
                HumanMessagePromptTemplate(
                    prompt=PromptTemplate(
                        input_variables=["input_dict_1", "input_dict_2"],
                        template=USER_PROMPT
                    )
                ),
            ]
        )

    def process(self, input_dict_1, input_dict_2):
        # Convert dicts to strings for prompt formatting
        input_dict_1_str = json.dumps(input_dict_1, indent=2)
        input_dict_2_str = json.dumps(input_dict_2, indent=2)

        messages = self.prompt_template.format_messages(
            input_dict_1=input_dict_1_str,
            input_dict_2=input_dict_2_str
        )

        response = self.llm(messages).content

        # Optional: Try to convert output string back to dictionary
        try:
            output_dict = json.loads(response)
            return output_dict
        except json.JSONDecodeError:
            return {"error": "Failed to parse LLM output as JSON", "raw_output": response}