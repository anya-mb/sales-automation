import logging
import os
from src.scraping.web_scraper_processor import WebScraperProcessor
from src.linkedin_user_processing import get_user_info
from src.utils import (
    LEAD_SUMMARY_AND_FACTS_FILENAME,
    save_lead_summary_and_facts,
    read_lead_summary_and_facts,
    setup_logging,
)
from src.generative_ai_utils import (
    build_rag,
    get_personalized_message,
    get_lead_facts_and_summary,
)


LOG_FILE_PATH = "logs/get_links_to_scrape.log"


def get_lead_facts(datapath: str, text: str) -> str:
    if not os.path.exists(os.path.join(datapath, LEAD_SUMMARY_AND_FACTS_FILENAME)):
        lead_facts_and_summary = get_lead_facts_and_summary(text)
        save_lead_summary_and_facts(datapath, lead_facts_and_summary)
    else:
        lead_facts_and_summary = read_lead_summary_and_facts(datapath)

    return lead_facts_and_summary


def process(company_url: str, user_id: str, style: str) -> str:
    setup_logging(LOG_FILE_PATH)
    logging.info(f"Company URL: {company_url}, User ID: {user_id}")

    web_scraper_processor = WebScraperProcessor(company_url)
    web_scraper_processor.run()

    datapath = web_scraper_processor.datapath

    rag_datapath = build_rag(web_scraper_processor.website_info, datapath)

    if not rag_datapath:
        raise FileNotFoundError

    company_facts_and_summary = web_scraper_processor.get_company_facts()

    lead_info = get_user_info(datapath, user_id)

    lead_facts_and_summary = get_lead_facts_and_summary(datapath, lead_info, user_id)

    personalised_message = get_personalized_message(
        datapath,
        user_id,
        company_facts_and_summary,
        lead_facts_and_summary,
        rag_datapath,
        style,
    )
    logging.info(f"Personalised message: {personalised_message}")

    return personalised_message
