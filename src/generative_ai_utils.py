import re
import os
import openai
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import HumanMessage, SystemMessage
import logging
from src.prompts import (
    PERSONALIZED_MESSAGE_PROMPT,
    COMPANY_SUMMARY_SYSTEM_PROMPT,
    LEAD_SUMMARY_SYSTEM_PROMPT,
)
from src.utils import (
    save_lead_summary_and_facts,
    read_lead_summary_and_facts,
    LEAD_SUMMARY_AND_FACTS_FILENAME,
    save_lead_personalized_message,
)
import warnings

warnings.filterwarnings("ignore")

# Load environment variables from .env file
_ = load_dotenv(find_dotenv())

# Set OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# LLM model configuration
llm_model = "gpt-3.5-turbo"

# Context window configuration for LLM
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
    """
    Clean LLM output by extracting content within the first and last curly braces.

    Args:
        llm_output (str): Output text from LLM.

    Returns:
        str: Cleaned LLM output.
    """
    cleaned_output = re.sub(
        r"^.*?({.*}).*$", r"\1", llm_output.lower(), flags=re.DOTALL
    )
    return cleaned_output


def build_rag(website_info: str, datapath: str) -> bool:
    """
    Build RAG (Retrieve, Aggregate, Generate) model.

    Args:
        website_info (str): Information from the website.
        datapath (str): Path to save RAG model data.

    Returns:
        bool: True if successful, False otherwise.
    """
    # Implementation to save RAG model data
    return True


def get_facts_and_summary(text: str, system_prompt: str) -> str:
    """
    Generate facts and summary using LLM.

    Args:
        text (str): Input text to generate facts and summary.
        system_prompt (str): System prompt template for LLM.

    Returns:
        str: Generated facts and summary.
    """
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
    """
    Truncate input text to fit within the context window for LLM.

    Args:
        text (str): Input text to truncate.
        context_window_char_len (int): Maximum length of context window.

    Returns:
        str: Truncated text.
    """
    if len(text) > context_window_char_len:
        logging.error(
            f"For LLM prompt, Text len: {len(text)} exceeds MAX_NUMBER_OF_CHARACTERS_IN_CONTEXT_WINDOW: {MAX_NUMBER_OF_CHARACTERS_IN_CONTEXT_WINDOW}. Truncating input."
        )
        text = text[:context_window_char_len]
    else:
        logging.info(f"For LLM prompt, Text len: {len(text)} is within context window.")
    return text


def get_company_facts_and_summary(text: str) -> str:
    """
    Generate company facts and summary using LLM.

    Args:
        text (str): Input text to generate company facts and summary.

    Returns:
        str: Generated company facts and summary.
    """
    text = truncate_to_context_window(text)
    company_facts_and_summary = get_facts_and_summary(
        text, COMPANY_SUMMARY_SYSTEM_PROMPT
    )
    return company_facts_and_summary


def get_lead_facts_and_summary(path: str, text: str, user_id: str) -> str:
    """
    Generate lead facts and summary using LLM.

    Args:
        path (str): Path to the user's folder.
        text (str): Input text to generate lead facts and summary.
        user_id (str): User ID to identify the user.

    Returns:
        str: Generated lead facts and summary.
    """
    user_folder = os.path.join(path, user_id)
    if not os.path.exists(os.path.join(user_folder, LEAD_SUMMARY_AND_FACTS_FILENAME)):
        lead_facts_and_summary = get_facts_and_summary(text, LEAD_SUMMARY_SYSTEM_PROMPT)
        save_lead_summary_and_facts(user_folder, lead_facts_and_summary)
        logging.info("Created lead_facts_and_summary")
    else:
        lead_facts_and_summary = read_lead_summary_and_facts(user_folder)
        logging.info("Read lead_facts_and_summary")
    return lead_facts_and_summary


def get_personalized_message(
    path: str,
    user_id: str,
    company_facts_and_summary: str,
    lead_facts_and_summary: str,
    rag_datapath: str,
    style="friendly",
) -> str:
    """
    Generate personalized message using LLM.

    Args:
        path (str): Path to the user's folder.
        user_id (str): User ID to identify the user.
        company_facts_and_summary (str): Company facts and summary.
        lead_facts_and_summary (str): Lead facts and summary.
        rag_datapath (str): Path to RAG model data.
        style (str, optional): Style of the personalized message. Defaults to "friendly".

    Returns:
        str: Generated personalized message.
    """
    prompt_template = PromptTemplate.from_template(PERSONALIZED_MESSAGE_PROMPT)
    model = ChatOpenAI(model=llm_model, temperature=0.5)
    chain = LLMChain(llm=model, prompt=prompt_template)
    personalized_message = chain.run(
        company_facts_and_summary=company_facts_and_summary,
        lead_facts_and_summary=lead_facts_and_summary,
        style=style,
    )
    logging.info(
        f"Created personalized message with LLM, size: {len(personalized_message)}"
    )
    user_folder = os.path.join(path, user_id)
    save_lead_personalized_message(user_folder, personalized_message)
    return personalized_message
