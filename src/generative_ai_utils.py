import re
import os
import openai
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
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
    WEBSITE_INFO_FILENAME,
)
import warnings
from typing import List

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

RAG_FOLDER_NAME = "RAG"
FAISS_FOLDER_NAME = "faiss_index"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
MIN_CHUNK_LENGTH = 100


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


def filter_chunks(docs: List[str]) -> List[str]:
    """
    Filter and select relevant document chunks.

    Args:
        docs (List[str]): List of document chunks.

    Returns:
        List[str]: List of filtered and selected document chunks.
    """
    selected_docs = []

    for doc in docs:
        if (
            doc.page_content not in selected_docs
            and len(doc.page_content) >= MIN_CHUNK_LENGTH
        ):
            selected_docs.append(doc.page_content)

    logging.info(
        f"Number of relevant chunks found: {len(selected_docs)}, total length: {sum([len(chunk) for chunk in selected_docs])}"
    )
    return selected_docs


def get_faiss_foldername(path: str) -> str:
    """
    Get the FAISS folder name.

    Args:
        path (str): Path to the base directory.

    Returns:
        str: FAISS folder name.
    """
    return os.path.join(path, RAG_FOLDER_NAME, FAISS_FOLDER_NAME)


def create_vector_db(path: str) -> object:
    """
    Create FAISS vector database from documents.

    Args:
        path (str): Path to the base directory.

    Returns:
        object: FAISS vector database object.
    """
    website_txt_path = os.path.join(path, WEBSITE_INFO_FILENAME)
    loader = TextLoader(website_txt_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    docs = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()

    db = FAISS.from_documents(docs, embeddings)
    logging.info(f"Created FAISS vector db, #chunks: {db.index.ntotal}")
    faiss_folder_name = get_faiss_foldername(path)
    db.save_local(faiss_folder_name)
    logging.info(f"FAISS vector db saved at: {faiss_folder_name}")
    return db


def load_vector_db(path: str) -> object:
    """
    Load FAISS vector database from disk.

    Args:
        path (str): Path to the base directory.

    Returns:
        object: FAISS vector database object.
    """
    rag_storage_folder = get_faiss_foldername(path)
    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local(
        rag_storage_folder, embeddings, allow_dangerous_deserialization=True
    )
    logging.info(f"FAISS vector db loaded from: {rag_storage_folder}")
    return db


def create_or_get_vector_db(path: str) -> object:
    """
    Create or load FAISS vector database.

    Args:
        path (str): Path to the base directory.

    Returns:
        object: FAISS vector database object.
    """
    rag_storage_folder = get_faiss_foldername(path)

    if os.path.exists(rag_storage_folder):
        db = load_vector_db(path)
    else:
        db = create_vector_db(path)
    return db


def get_rag_chunks(user_information: str, path: str) -> List[str]:
    """
    Get relevant RAG chunks for the user.

    Args:
        user_information (str): User information for RAG retrieval.
        path (str): Path to the base directory.

    Returns:
        List[str]: List of relevant RAG chunks.
    """
    db = create_or_get_vector_db(path)

    docs = db.similarity_search(user_information, k=6)
    selected_chunks = filter_chunks(docs)

    logging.info(f"# selected RAG chunks: {len(selected_chunks)}")

    return selected_chunks


def get_personalized_message(
    path: str,
    user_id: str,
    company_facts_and_summary: str,
    lead_facts_and_summary: str,
    style: str,
    additional_notes: str,
) -> str:
    """
    Generate personalized message using LLM.

    Args:
        path (str): Path to the company's folder.
        user_id (str): User ID to identify the user.
        company_facts_and_summary (str): Company facts and summary.
        lead_facts_and_summary (str): Lead facts and summary.
        style (str): Style of the personalized message.
        additional_notes (str): Additional notes for the message.

    Returns:
        str: Generated personalized message.
    """
    prompt_template = PromptTemplate.from_template(PERSONALIZED_MESSAGE_PROMPT)
    model = ChatOpenAI(model=llm_model, temperature=0.5)

    rag_chunks = get_rag_chunks(lead_facts_and_summary, path)

    prompt = prompt_template.format(
        company_facts_and_summary=company_facts_and_summary,
        lead_facts_and_summary=lead_facts_and_summary,
        rag_chunks=rag_chunks,
        style=style,
        additional_notes=additional_notes,
    )

    logging.info(f"Prompt: {prompt}")
    result = model.invoke([SystemMessage(content=prompt)])

    personalized_message = result.content

    logging.info(
        f"Created personalized message with LLM, size: {len(personalized_message)}"
    )

    user_folder = os.path.join(path, user_id)
    save_lead_personalized_message(user_folder, personalized_message)
    return personalized_message
