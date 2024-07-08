import os
from typing import List

from generative_ai_utils import get_company_facts_and_summary
from scraping.extract_all_links_and_summary_text import (
    find_best_links_for_summary,
    fetch_html_website_and_summary_content,
)
from scraping.get_links_to_scrape import get_all_links
from utils import *

DEPTH_TO_SCRAPE = 2
N_MAX_SUMMARY_LINKS = 10


class WebScraperProcessor:
    def __init__(self, url: str):
        self.summary_info = None
        self.website_info = None
        self.url = url
        self.datapath = get_url_datapath(url, create=True)

    def run(self):
        all_links = scrape_or_load_all_links(self.datapath, self.url)
        summary_links = create_or_load_summary_links(self.datapath, all_links)

        website_info, summary_info = fetch_or_load_html_website_and_summary_content(
            self.datapath, all_links, summary_links
        )
        self.website_info, self.summary_info = website_info, summary_info

    def get_company_facts(self) -> str:
        if not os.path.exists(
            os.path.join(self.datapath, COMPANY_SUMMARY_AND_FACTS_FILENAME)
        ):
            company_facts_and_summary = get_company_facts_and_summary(self.summary_info)
            save_company_summary_and_facts(self.datapath, company_facts_and_summary)
        else:
            company_facts_and_summary = read_company_summary_and_facts(self.datapath)

        return company_facts_and_summary


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
    if not (
        os.path.exists(os.path.join(datapath, WEBSITE_INFO_FILENAME))
        or os.path.exists(os.path.join(datapath, WEBSITE_SUMMARY_INFO_FILENAME))
    ):

        website_info, summary_info = fetch_html_website_and_summary_content(
            all_links, summary_links
        )
        save_website_info(datapath, website_info)
        save_summary_info(datapath, summary_info)

    else:
        website_info = read_website_info(datapath)
        summary_info = read_summary_info(datapath)

    return website_info, summary_info