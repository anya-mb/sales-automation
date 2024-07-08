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
    WEBSITE_INFO_FILENAME,
    WEBSITE_SUMMARY_INFO_FILENAME,
    save_website_info,
    save_summary_info,
    read_website_info,
    read_summary_info,
    save_company_summary_and_facts,
    read_company_summary_and_facts,
    COMPANY_SUMMARY_AND_FACTS_FILENAME,
    LEAD_SUMMARY_AND_FACTS_FILENAME,
    save_lead_summary_and_facts,
    read_lead_summary_and_facts,
)
from extract_all_links_and_summary_text import (
    find_best_links_for_summary,
    fetch_html_website_and_summary_content,
)
from generative_ai_utils import (
    build_rag,
    get_presonalised_message,
    get_company_facts_and_summary,
    get_lead_facts_and_summary,
)

# from linkedin_extraction import get_user_info
import os
from typing import List


LOG_FILE_PATH = "../logs/get_links_to_scrape.log"
DEPTH_TO_SCRAPE = 2
N_MAX_SUMMARY_LINKS = 10
LINKEDIN_LOGIN = ""
LINKEDIN_PASSWORD = ""


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


def fetch_or_load_html_website_and_summary_content(
    datapath: str, all_links: List[str], summary_links: List[str]
) -> tuple[str, str]:

    if not os.path.exists(
        os.path.join(datapath, WEBSITE_INFO_FILENAME)
    ) or os.path.exists(os.path.join(datapath, WEBSITE_SUMMARY_INFO_FILENAME)):

        website_info, summary_info = fetch_html_website_and_summary_content(
            all_links, summary_links
        )
        save_website_info(datapath, website_info)
        save_summary_info(datapath, summary_info)

    else:
        website_info = read_website_info(datapath)
        summary_info = read_summary_info(datapath)

    return website_info, summary_info


def get_or_load_company_facts(datapath: str, text: str) -> str:
    if not os.path.exists(os.path.join(datapath, COMPANY_SUMMARY_AND_FACTS_FILENAME)):
        company_facts_and_summary = get_company_facts_and_summary(text)
        save_company_summary_and_facts(datapath, company_facts_and_summary)
    else:
        company_facts_and_summary = read_company_summary_and_facts(datapath)

    return company_facts_and_summary


def get_or_load_lead_facts(datapath: str, text: str) -> str:
    if not os.path.exists(os.path.join(datapath, LEAD_SUMMARY_AND_FACTS_FILENAME)):
        lead_facts_and_summary = get_lead_facts_and_summary(text)
        save_lead_summary_and_facts(datapath, lead_facts_and_summary)
    else:
        lead_facts_and_summary = read_lead_summary_and_facts(datapath)

    return lead_facts_and_summary


def process():
    # Parse command-line arguments
    args = parse_arguments()
    url = args.url

    setup_logging(LOG_FILE_PATH)
    logging.info(f"URL: {url}")

    datapath = get_url_datapath(url, create=True)

    all_links = scrape_or_load_all_links(datapath, url)
    summary_links = create_or_load_summary_links(datapath, all_links)

    website_info, summary_info = fetch_or_load_html_website_and_summary_content(
        datapath, all_links, summary_links
    )

    rag_datapath = build_rag(website_info, datapath)

    if not rag_datapath:
        raise FileNotFoundError

    company_facts_and_summary = get_or_load_company_facts(datapath, summary_info)

    # lead_info = get_user_info(LINKEDIN_LOGIN, LINKEDIN_PASSWORD)

    lead_facts_and_summary = ""  # get_lead_facts_and_summary(datapath, lead_info)

    personalised_message = get_presonalised_message(
        company_facts_and_summary, lead_facts_and_summary, rag_datapath
    )
    print(f"Personalised message: {personalised_message}")

    return personalised_message


if __name__ == "__main__":
    process()
