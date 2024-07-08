import re
import os
import openai
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import logging

# from utils import save_company_summary_and_facts, read_company_summary_and_facts


_ = load_dotenv(find_dotenv())  # read local .env file
openai.api_key = os.environ["OPENAI_API_KEY"]

# llm_model = "gpt-3.5-turbo"
llm_model = "gpt-4o"

COMPANY_SUMMARY_SYSTEM_PROMPT = """
I have provided the text scraped from a company website. Please create a detailed summary and list up to 10 facts about the company. These facts should include information about the company's products, advantages of using their products, useful features, company values, and other positive aspects. The summary and list should be concise and informative.

Example of Output:

Summary:
[Detailed summary of the company based on the provided text]

Facts:

1. [Fact about the company's products]
2. [Fact about the advantages of using the company's products]
3. [Fact about useful features of the company's products]
4. [Fact about the company's values]
5. [Fact about the company's values or positive aspects]
6. [Fact about the company's positive aspects]
7. [Fact about the company's products or features]
8. [Fact about the company's products or features]
9. [Fact about the company's values or positive aspects]
10. [Fact about the company's products, features, or values]

My life depends on this. I will tip you generously if you follow the instructions and do a great job.
"""

LEAD_SUMMARY_SYSTEM_PROMPT = """
I have provided the text about a person. Please create a detailed summary and list up to 10 facts about this person. These facts should include information about their interests, career, and activities. The summary and list should be concise and informative.

Example of Output:

Summary:
[Detailed summary of the person based on the provided text]

Facts:

1. [Fact about the person's interests]
2. [Fact about the person's career]
3. [Fact about the person's activities]
4. [Fact about the person's interests or hobbies]
5. [Fact about the person's professional achievements]
6. [Fact about the person's involvement in activities]
7. [Fact about the person's career milestones]
8. [Fact about the person's personal interests]
9. [Fact about the person's notable activities or hobbies]
10. [Fact about the person's professional or personal life]

My life depends on this. I will tip you generously if you follow the instructions and do a great job.
"""

# GPT 3.5 turbo
CONTEXT_WINDOW_GPT35 = 16_385
N_CHARACTERS_PER_TOKEN = 4
SAFE_COEF = 0.9
MAX_NUMBER_OF_CHARACTERS_IN_CONTEXT_WINDOW = int(
    SAFE_COEF
    * (
        CONTEXT_WINDOW_GPT35 * N_CHARACTERS_PER_TOKEN
        - max(len(COMPANY_SUMMARY_SYSTEM_PROMPT), len(LEAD_SUMMARY_SYSTEM_PROMPT))
    )
)

# # GPT4o
# CONTEXT_WINDOW_GPT = 100_000 # 128_000
# N_CHARACTERS_PER_TOKEN = 4
# SAFE_COEF = 0.8
# MAX_NUMBER_OF_CHARACTERS_IN_CONTEXT_WINDOW = int(SAFE_COEF * (CONTEXT_WINDOW_GPT * N_CHARACTERS_PER_TOKEN - max(len(COMPANY_SUMMARY_SYSTEM_PROMPT), len(LEAD_SUMMARY_SYSTEM_PROMPT))))


def clean_llm_output(llm_output: str) -> str:
    # Use regex to remove everything before the first { and after the last }
    cleaned_output = re.sub(
        r"^.*?({.*}).*$", r"\1", llm_output.lower(), flags=re.DOTALL
    )
    return cleaned_output


def build_rag(website_info: str, datapath: str) -> bool:
    # save to datapath and rag_directory
    return True


def get_facts_and_summary(summary_info: str, system_prompt: str) -> str:
    # generates facts and summary with LLM

    chat = ChatOpenAI(
        temperature=0.2,
        model=llm_model,
    )

    result = chat.invoke(
        [SystemMessage(content=system_prompt), HumanMessage(content=summary_info)]
    )

    logging.info(f"Created facts and summary with LLM, size: {len(result.content)}")

    return result.content


def truncate_to_context_window(
    text: str, context_window_char_len: int = MAX_NUMBER_OF_CHARACTERS_IN_CONTEXT_WINDOW
) -> str:
    if len(text) > context_window_char_len:
        logging.error(
            f"For LLM prompt, Text len: {len(text)} while MAX_NUMBER_OF_CHARACTERS_IN_CONTEXT_WINDOW: {MAX_NUMBER_OF_CHARACTERS_IN_CONTEXT_WINDOW}, will truncate input to it"
        )
        text = text[:context_window_char_len]
    else:
        logging.info(
            f"For LLM prompt, Text len: {len(text)} which is within context window"
        )
    return text


def get_company_facts_and_summary(text: str) -> str:
    text = truncate_to_context_window(text)

    company_facts_and_summary = get_facts_and_summary(
        text, COMPANY_SUMMARY_SYSTEM_PROMPT
    )
    logging.info(f"Created company_facts_and_summary: {company_facts_and_summary}")
    return company_facts_and_summary


def get_lead_facts_and_summary(text: str) -> str:
    text = truncate_to_context_window(text)

    lead_facts_and_summary = get_facts_and_summary(text, LEAD_SUMMARY_SYSTEM_PROMPT)
    logging.info(f"Created lead_facts_and_summary: {lead_facts_and_summary}")
    return lead_facts_and_summary


def get_presonalised_message(
    company_facts_and_summary: str, lead_facts_and_summary: str, rag_datapath: str
) -> str:
    # prompt for LLM with company_facts_and_summary, lead_facts_and_summary and rag chuncks
    return "You're the best! Buy out product!"
