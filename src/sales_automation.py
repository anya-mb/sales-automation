import logging

from scraping.web_scraper_processor import WebScraperProcessor
from linkedin_extraction import get_user_info
from utils import setup_logging
from utils import (
    # save_company_summary_and_facts,
    # read_company_summary_and_facts,
    # COMPANY_SUMMARY_AND_FACTS_FILENAME,
    LEAD_SUMMARY_AND_FACTS_FILENAME,
    save_lead_summary_and_facts,
    read_lead_summary_and_facts,
)
from generative_ai_utils import (
    build_rag,
    get_presonalised_message,
    # get_company_facts_and_summary,
    get_lead_facts_and_summary,
)

# from linkedin_extraction import get_user_info
import os

LOG_FILE_PATH = "../logs/get_links_to_scrape.log"

LINKEDIN_LOGIN = ""
LINKEDIN_PASSWORD = ""


def get_lead_facts(datapath: str, text: str) -> str:
    if not os.path.exists(os.path.join(datapath, LEAD_SUMMARY_AND_FACTS_FILENAME)):
        lead_facts_and_summary = get_lead_facts_and_summary(text)
        save_lead_summary_and_facts(datapath, lead_facts_and_summary)
    else:
        lead_facts_and_summary = read_lead_summary_and_facts(datapath)

    return lead_facts_and_summary


def process(url: str) -> str:
    setup_logging(LOG_FILE_PATH)
    logging.info(f"URL: {url}")

    web_scraper_processor = WebScraperProcessor(url)
    web_scraper_processor.run()

    rag_datapath = build_rag(
        web_scraper_processor.website_info, web_scraper_processor.datapath
    )

    if not rag_datapath:
        raise FileNotFoundError

    company_facts_and_summary = web_scraper_processor.get_company_facts()

    user_id = "andrew-huberman"

    lead_info = get_user_info(user_id)

    lead_facts_and_summary = get_lead_facts_and_summary(
        web_scraper_processor.datapath, lead_info, user_id
    )

    personalised_message = get_presonalised_message(
        web_scraper_processor.datapath,
        company_facts_and_summary,
        lead_facts_and_summary,
        rag_datapath,
    )
    print(f"Personalised message: {personalised_message}")

    return personalised_message
