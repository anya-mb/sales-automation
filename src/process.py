import argparse
import logging
from utils import setup_logging
from get_links_to_scrape import get_all_links
from utils import (
    save_all_links,
    read_all_links,
    save_summary_links,
    read_summary_links,
    get_url_datapath,
    ALL_LINKS_FILENAME,
    SUMMARY_LINKS_FILENAME,
)
from extract_all_links_and_summary_text import (
    find_best_links_for_summary,
    fetch_html_website_and_summary_content,
)
from generative_ai_utils import (
    build_rag,
    get_facts_and_summary,
    get_presonalised_message,
)
from linkedin_extraction import get_user_info
import os
from typing import List


LOG_FILE_PATH = "../logs/get_links_to_scrape.log"


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
        "--url",
        type=str,
        default="https://www.therocketbrew.com",
        help="URL to find links on and save them",
    )
    parser.add_argument(
        "--depth", type=int, default=2, help="The depth to go to find links to scrape"
    )

    return parser.parse_args()


def create_url_datapath(url: str, create: bool = True) -> str:
    # domain_folder_name = get_domain_data_folder(url)

    # # Determine the output directory
    # domain_folder_name_relative = args.path_to_save or os.path.join(
    #     "../data", domain_folder_name
    # )
    # os.makedirs(domain_folder_name_relative, exist_ok=True)

    # # Extract links and save them to a JSON file
    # links = get_all_links(args.url, args.depth)
    # logging.info(
    #     f"Extracted {len(links)} links from URL: {args.url} with depth: {args.depth}"
    # )

    # links_data = {"all_links": links}
    # file_path_to_save = os.path.join(
    #     domain_folder_name_relative, f"all_links_depth_{args.depth}.json"
    # )
    return ""


def scrape_or_load_all_links(datapath: str, url: str) -> List[str]:
    # no scraping if scraped
    if not os.path.exists(os.path.join(datapath, ALL_LINKS_FILENAME)):
        all_links = get_all_links(url, depth=DEPTH_TO_SCRAPE)

        # Save links to json file
        save_all_links(datapath, all_links)

    else:
        all_links = read_all_links(datapath)

    return all_links


def create_or_load_summary_links(datapath: str, all_links: List[str]) -> List[str]:
    if not os.path.exists(os.path.join(datapath, SUMMARY_LINKS_FILENAME)):
        summary_links = find_best_links_for_summary(all_links)[:N_MAX_SUMMARY_LINKS]
        save_summary_links(datapath, all_links)
    else:
        summary_links = read_summary_links(datapath)

    return summary_links


DEPTH_TO_SCRAPE = 2
N_MAX_SUMMARY_LINKS = 10
LINKEDIN_LOGIN = ""
LINKEDIN_PASSWORD = ""


def process():
    # Parse command-line arguments
    args = parse_arguments()
    url = args.url

    setup_logging(LOG_FILE_PATH)
    logging.info(f"URL: {url}")

    datapath = get_url_datapath(url)

    if not os.path.exists(datapath):
        os.makedirs(datapath)
        logging.info(f"Directory created: {datapath}")

    all_links = scrape_or_load_all_links(datapath, url)
    summary_links = create_or_load_summary_links(datapath, all_links)

    website_info, summary_info = fetch_html_website_and_summary_content(
        all_links, summary_links
    )

    rag_datapath = build_rag(website_info, datapath)

    if not rag_datapath:
        raise FileNotFoundError

    company_facts_and_summary = get_facts_and_summary(summary_info)

    lead_info = get_user_info(LINKEDIN_LOGIN, LINKEDIN_PASSWORD)

    lead_facts_and_summary = get_facts_and_summary(lead_info)

    personalised_message = get_presonalised_message(
        company_facts_and_summary, lead_facts_and_summary, rag_datapath
    )
    print(f"Personalised message: {personalised_message}")

    return personalised_message


if __name__ == "__main__":
    process()
