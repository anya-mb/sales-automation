import json
from typing import List, Tuple
import os
import argparse
import logging
import requests
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv, find_dotenv
from src.generative_ai_utils import clean_llm_output
from src.utils import setup_logging, read_links, save_links
import openai

# Load environment variables
_ = load_dotenv(find_dotenv())

# OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Path for logging
LOG_FILE_PATH = "../../logs/extract_all_links_and_summary_text.log"

# Language model for summarization
LLM_MODEL = "gpt-3.5-turbo"

# Prompt for system to select best links for summary
SUMMARY_SYSTEM_PROMPT = """
I'm scraping this website to learn about the product offerings, benefits, and competitive advantages of this company or its products.
Please help me choose the most useful links to scrape first. I'll send you links.
Return JSON with key "useful_links" and value as list of links, no other text is needed.
"""


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the script.

    Returns:
        argparse.Namespace: Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Extract links and summaries from provided URLs."
    )

    parser.add_argument(
        "--path_to_read",
        type=str,
        default="../data/www_therocketbrew_com/all_links_depth_2.json",
        help="Path to read JSON file containing links",
    )

    return parser.parse_args()


def find_best_links_for_summary(all_links: List[str], n_links: int = 10) -> List[str]:
    """
    Use OpenAI's ChatOpenAI with a specific prompt to select the best links for summarization.

    Args:
        all_links (List[str]): List of all links to consider.
        n_links (int): Number of links to select for summarization.

    Returns:
        List[str]: List of selected links.
    """
    chat = ChatOpenAI(temperature=0, model=LLM_MODEL)

    result = chat.invoke(
        [
            SystemMessage(content=SUMMARY_SYSTEM_PROMPT),
            HumanMessage(content=json.dumps(all_links)),
        ]
    )

    clean_output = clean_llm_output(result.content)

    llm_links = json.loads(clean_output)
    summary_links = llm_links["useful_links"]

    logging.info(f"Selected summary links: {summary_links}")

    return summary_links


def fetch_html_content_one_url(url: str) -> str:
    """
    Fetch HTML content from a given URL.

    Args:
        url (str): URL of the website.

    Returns:
        str: Raw HTML content of the page.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad status codes

        # Parse HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        return soup.get_text()
    except requests.RequestException as e:
        logging.error(f"Error fetching URL {url}: {e}")
        return ""


def fetch_html_website_and_summary_content(
    all_links: List[str], summary_links: List[str]
) -> Tuple[str, str]:
    """
    Fetch HTML content for all links and extract website and summary information.

    Args:
        all_links (List[str]): List of all links to scrape.
        summary_links (List[str]): List of selected links for summarization.

    Returns:
        Tuple[str, str]: Tuple containing website information and summary information.
    """
    website_info = ""
    summary_info = ""

    for link in all_links:
        html_content = fetch_html_content_one_url(link)
        html_content += " \n "
        website_info += html_content

        if link in summary_links:
            summary_info += html_content

    logging.info(
        f"Scraped website info length: {len(website_info)}, summary length: {len(summary_info)}"
    )

    return website_info, summary_info


def main():
    """
    Main function to orchestrate link extraction and summary scraping.
    """
    args = parse_arguments()
    setup_logging(LOG_FILE_PATH)

    all_links = read_links(args.path_to_read)

    N_MAX_SUMMARY_LINKS = 10
    summary_links = find_best_links_for_summary(all_links)[:N_MAX_SUMMARY_LINKS]
    logging.info(f"Selected summary links: {summary_links}")

    summary_links_data = {"summary_links": summary_links}
    file_path_to_save = os.path.dirname(args.path_to_read)

    # Save summary links to a JSON file
    save_links(
        os.path.join(file_path_to_save, "summary_links.json"), summary_links_data
    )

    website_info, summary_info = fetch_html_website_and_summary_content(
        all_links, summary_links
    )

    # Save scraped website content and summary to text files
    with open(os.path.join(file_path_to_save, "website_info.txt"), "w") as file:
        file.write(website_info)
    logging.info(
        f"Scraped website saved to: {os.path.join(file_path_to_save, 'website_info.txt')}"
    )

    with open(os.path.join(file_path_to_save, "website_summary_info.txt"), "w") as file:
        file.write(summary_info)
    logging.info(
        f"Scraped website summary saved to: {os.path.join(file_path_to_save, 'website_summary_info.txt')}"
    )


if __name__ == "__main__":
    main()
