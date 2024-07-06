import json
from typing import List
import os
import openai
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv, find_dotenv
from generative_ai_utils import SUMMARY_SYSTEM_PROMPT, clean_llm_output
import requests
from bs4 import BeautifulSoup

# from typing import List
import argparse
from utils import setup_logging, read_links, save_links
import logging


_ = load_dotenv(find_dotenv())  # read local .env file
openai.api_key = os.environ["OPENAI_API_KEY"]

LOG_FILE_PATH = "../logs/extract_all_links_and_summary_text.log"

LLM_MODEL = "gpt-3.5-turbo"


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the script.

    Returns:
        argparse.Namespace: Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Get links to scrape from the provided URL"
    )

    parser.add_argument(
        "--path_to_read",
        type=str,
        default="../data/www_therocketbrew_com/all_links_depth_2.json",
        help="Path to read JSON file for links",
    )

    return parser.parse_args()


def find_best_links_for_summary(all_links: List[str], n_links: int = 10) -> List[str]:
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

    return summary_links


# def get_company_facts(summary: str) -> str:
#     #


# def save_summary_links():

#     summary_links_str_to_save = json.dumps({"summary_links": summary_links})

#     summary_links_filename = 'summary_links.json'

#     file_path_to_save = os.path.join(domain_folder_name, summary_links_filename)

#     # Write the JSON object to a file
#     with open(file_path_to_save, 'w') as json_file:
#         json.dump(summary_links_str_to_save, json_file, indent=4)


def fetch_html_content_one_url(url: str) -> str:
    """Fetch the HTML content from a given URL.

    Args:
        url (str): The URL of the website to fetch HTML content from.

    Returns:
        str: The raw HTML content of the page.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        return soup.get_text()
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return ""


def fetch_html_website_and_summary_content(
    all_links: List[str], summary_links: List[str]
) -> tuple[str, str]:
    website_info = ""
    summary_info = ""

    for link in all_links:

        html_content = fetch_html_content_one_url(link)
        website_info += html_content

        if link in summary_links:
            summary_info += html_content

    logging.info(
        f"Link: {link}, length of scraped website_info: {len(website_info)}, length of scraped summary: {len(summary_info)}"
    )

    return (website_info, summary_info)


def main():
    args = parse_arguments()
    setup_logging(LOG_FILE_PATH)

    all_links = read_links(args.path_to_read)

    N_MAX_SUMMARY_LINKS = 10
    summary_links = find_best_links_for_summary(all_links)[:N_MAX_SUMMARY_LINKS]
    logging.info(f"Summary links: {summary_links}")

    summary_links_data = {"summary_links": summary_links}

    file_path_to_save = args.path_to_read.rsplit("/", maxsplit=1)
    logging.info(f"File path to save: {file_path_to_save}")

    full_filepath_to_save = os.path.join(file_path_to_save, "summary_links.json")

    # Save summary links to json file
    save_links(full_filepath_to_save, summary_links_data)

    website_info = ""
    summary_info = ""

    for link in all_links:

        html_content = fetch_html_content_one_url(link)
        website_info += html_content

        if link in summary_links:
            summary_info += html_content

    logging.info(
        f"Link: {link}, length of scraped website_info: {len(website_info)}, length of scraped summary: {len(summary_info)}"
    )

    scraped_website_filepath = os.path.join(file_path_to_save, "website_info.txt")
    with open(scraped_website_filepath, "w") as file:
        file.write(website_info)

    logging.info(f"Scraped website saved to: {scraped_website_filepath}")

    with open(os.path.join(file_path_to_save, "website_summary_info.txt"), "w") as file:
        file.write(summary_info)

    logging.info(f"Scraped website summary saved to: {scraped_website_filepath}")


if __name__ == "__main__":
    main()
