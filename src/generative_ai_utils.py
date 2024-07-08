import re
import os
import openai
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import logging
from prompts import (
    # PERSONALIZED_MESSAGE_PROMPT,
    COMPANY_SUMMARY_SYSTEM_PROMPT,
    LEAD_SUMMARY_SYSTEM_PROMPT,
)


_ = load_dotenv(find_dotenv())  # read local .env file
openai.api_key = os.environ["OPENAI_API_KEY"]

llm_model = "gpt-3.5-turbo"
# llm_model = "gpt-4o"


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
    logging.info("Created company_facts_and_summary")
    return company_facts_and_summary


def get_lead_facts_and_summary(text: str) -> str:
    text = truncate_to_context_window(text)

    lead_facts_and_summary = get_facts_and_summary(text, LEAD_SUMMARY_SYSTEM_PROMPT)
    logging.info("Created lead_facts_and_summary")
    return lead_facts_and_summary


def get_presonalised_message(
    company_facts_and_summary: str, lead_facts_and_summary: str, rag_datapath: str
) -> str:
    # prompt for LLM with company_facts_and_summary, lead_facts_and_summary and rag chuncks
    return "You're the best! Buy out product!"
