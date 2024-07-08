import re
import os
import openai
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import logging
from prompts import (
    PERSONALIZED_MESSAGE_PROMPT,
    COMPANY_SUMMARY_SYSTEM_PROMPT,
    LEAD_SUMMARY_SYSTEM_PROMPT,
)
from utils import LEAD_SUMMARY_FILENAME, save_lead_summary, read_lead_summary


_ = load_dotenv(find_dotenv())  # read local .env file
openai.api_key = os.environ["OPENAI_API_KEY"]

llm_model = "gpt-3.5-turbo"

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


def clean_llm_output(llm_output: str) -> str:
    # Use regex to remove everything before the first { and after the last }
    cleaned_output = re.sub(
        r"^.*?({.*}).*$", r"\1", llm_output.lower(), flags=re.DOTALL
    )
    return cleaned_output


def build_rag(website_info: str, datapath: str) -> bool:
    # save to datapath and rag_directory
    return True


def get_facts_and_summary(text: str, system_prompt: str) -> str:
    # generates facts and summary with LLM

    chat = ChatOpenAI(
        temperature=0.2,
        model=llm_model,
    )

    result = chat.invoke(
        [SystemMessage(content=system_prompt), HumanMessage(content=text)]
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


def get_lead_facts_and_summary(path: str, text: str, user_id: str) -> str:
    if not os.path.exists(os.path.join(path, "user_id" + LEAD_SUMMARY_FILENAME)):
        lead_facts_and_summary = get_facts_and_summary(text, LEAD_SUMMARY_SYSTEM_PROMPT)
        save_lead_summary(path, lead_facts_and_summary, user_id)
        logging.info("Created lead_facts_and_summary")
    else:
        lead_facts_and_summary = read_lead_summary(path, user_id)
        logging.info("Read lead_facts_and_summary")

    return lead_facts_and_summary


def get_presonalised_message(
    path: str,
    company_facts_and_summary: str,
    lead_facts_and_summary: str,
    rag_datapath: str,
    style="friendly",
) -> str:
    message = (
        f"Company facts and summary:\n{company_facts_and_summary}\n"
        + f"User Facts and Summary:\n{lead_facts_and_summary}\n"
        + f"Style:\n{style}"
    )

    text = truncate_to_context_window(message)

    chat = ChatOpenAI(
        temperature=0.2,
        model=llm_model,
    )

    result = chat.invoke(
        [SystemMessage(content=PERSONALIZED_MESSAGE_PROMPT), HumanMessage(content=text)]
    )

    personalized_message = result.content

    logging.info(
        f"Created personalized message with LLM, size: {len(personalized_message)}"
    )

    return personalized_message
