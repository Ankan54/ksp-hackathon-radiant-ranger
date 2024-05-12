from langchain_google_genai import ChatGoogleGenerativeAI
import os
from process_data import PostAnalysis
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()


gemini_llm = ChatGoogleGenerativeAI(model="gemini-pro", max_output_tokens=2048,temperature=0)

gemini_parser = PydanticOutputParser(pydantic_object=PostAnalysis)

gemini_prompt = PromptTemplate(
    template="You are provided with a social media post posted by a human user with triple backquotes, reporting some event occuring in a place. Think carefully, and then generate response as per the instruction. The responses will be analysed by Police perssonels to identify related events, so that they can take prompt action on it. The output should be in a JSON format as per the given instructions below\n{format_instructions}\n```{input}```\nOUTPUT JSON:",
    input_variables=["input"],
    partial_variables={"format_instructions": gemini_parser.get_format_instructions()},
)

gemini_chain = gemini_prompt | gemini_llm | gemini_parser


def gemini_process_post(input_str):
    try:
        output = gemini_chain.invoke({"input": input_str})
        return output
    except Exception as e:
        print(f"Error: str(e)")
        return False